from django.urls import path
from statistic.views import StatisticsPage, statistics_tags_api

urlpatterns = [
    path("tags/", statistics_tags_api, name="stats_tags"),
    path("", StatisticsPage.as_view(), name="statistics")
]
