from django.urls import path

from . import views


urlpatterns = [
    path('teaser_status/', views.TeaserChangeStatusView.as_view(), name='teaser_status'),
]
