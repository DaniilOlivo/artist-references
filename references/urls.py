from django.urls import path
from references.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]

