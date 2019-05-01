from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
]