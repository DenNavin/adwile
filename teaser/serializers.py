from rest_framework import serializers

from teaser.config import STATUSES_PAID


class TeaserChangeStatusSerializer(serializers.Serializer):
    """Сериализация данных при смене статуса тизеров"""

    teaser_ids = serializers.ListField(child=serializers.IntegerField(min_value=1))
    status_paid = serializers.ChoiceField(choices=[STATUSES_PAID['paid'], STATUSES_PAID['reject']])

