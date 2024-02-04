from django.urls import path
from statistic.views import StatisticsPage

urlpatterns = [
    path("", StatisticsPage.as_view(), name="statistics")
]
