from django.urls import path
from references.views import IndexView, reference_list

urlpatterns = [
    path("list/", reference_list, name="references"),
    path("", IndexView.as_view(), name="index"),
]

