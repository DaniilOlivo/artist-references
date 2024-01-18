from django.urls import path
from login.views import LoginPageView, RegisterPageView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", LoginPageView.as_view(), name="login"),
    path("register/", RegisterPageView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
