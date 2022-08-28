from django.urls import path
from account.views import UserRegistractionView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswodResetEmailView, UserPasswordResetView



urlpatterns = [
  
    path('register/',UserRegistractionView.as_view(),name="register"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('profile/',UserProfileView.as_view(),name="profile"),
    path('changepass/',UserChangePasswordView.as_view(),name="changepass"),
    path('send-reset-password-email/',SendPasswodResetEmailView.as_view(),name="send-reset-password-email"),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password")
]