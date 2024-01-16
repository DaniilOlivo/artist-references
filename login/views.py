from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

class LoginPageView(LoginView):
    extra_context = {"active_section": "login", "part": "login"}
    template_name = 'login/login.html'

class RegisterPageView(CreateView):
    extra_context = {"active_section": "register", "part": "login"}
    template_name = 'login/register.html'
    model = User
    success_url = "/auth/login/"
    form_class = UserCreationForm
