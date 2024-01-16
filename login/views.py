from django.contrib.auth.views import LoginView

class LoginPageView(LoginView):
    template_name = 'login/login.html'
