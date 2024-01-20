from django.urls import path
from references.views import *

urlpatterns = [
    path("create/", CreateReferenceView.as_view(), name="create_reference"),
    path("edit/<int:pk>/", UpdateReferenceView.as_view(), name="edit_reference"),
    path("delete/<int:pk>/", DeleteReferenceView.as_view(), name="delete_reference"),
    path("list/", reference_list, name="references"),
    path("", IndexView.as_view(), name="index"),
]

