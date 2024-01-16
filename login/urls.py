from django.urls import path, re_path
from login.views import LoginPageView

urlpatterns = [
    path("login/", LoginPageView.as_view(), name="login"),
]
