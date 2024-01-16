from django.urls import path
from references.views import IndexView, ReferenceView

urlpatterns = [
    path("list/", ReferenceView.as_view(), name="references"),
    path("", IndexView.as_view(), name="index"),
]

