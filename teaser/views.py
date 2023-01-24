from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from teaser.serializers import TeaserChangeStatusSerializer
from teaser.services import change_teaser_status


class TeaserChangeStatusView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request):
        serializer = TeaserChangeStatusSerializer(data=request.data)
        if serializer.is_valid():
            teasers_data = change_teaser_status(
                teaser_ids=serializer.data['teaser_ids'], status_paid=serializer.data['status_paid'])

            return Response(data={'status': 'OK', 'teaser_data': teasers_data})

        return Response({'status': 'ERROR'})
