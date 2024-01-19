from django.urls import path
from references.views import IndexView, reference_list, CreateReferenceView

urlpatterns = [
    path("create/", CreateReferenceView.as_view(), name="create_reference"),
    path("list/", reference_list, name="references"),
    path("", IndexView.as_view(), name="index"),
]

