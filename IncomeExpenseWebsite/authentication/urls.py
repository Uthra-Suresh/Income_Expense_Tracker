from . views import RegistrationView, UsernameValidationView,EmailValidationView,LoginView, LogoutView,HomeView,DeleteAccountView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register',RegistrationView.as_view(),name="register"),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name="validate-username"),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name="validate-email"),
    path('login',csrf_exempt(LoginView.as_view()),name="login"),
    path('logout',csrf_exempt(LogoutView.as_view()),name="logout"),
    path('home',HomeView.as_view(),name="home"),
    path('delete_account',DeleteAccountView.as_view(),name="delete_account"),

    

]