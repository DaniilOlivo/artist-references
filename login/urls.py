from django.urls import path
from login.views import LoginPageView, RegisterPageView

urlpatterns = [
    path("login/", LoginPageView.as_view(), name="login"),
    path("register/", RegisterPageView.as_view(), name="register"),
]
