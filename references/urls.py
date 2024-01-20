from django.urls import path
from references.views import IndexView, reference_list, CreateReferenceView, UpdateReferenceView

urlpatterns = [
    path("create/", CreateReferenceView.as_view(), name="create_reference"),
    path("edit/<int:pk>/", UpdateReferenceView.as_view(), name="edit_reference"),
    path("list/", reference_list, name="references"),
    path("", IndexView.as_view(), name="index"),
]

