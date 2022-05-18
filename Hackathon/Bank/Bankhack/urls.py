"""Bankhack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from .views import login
#from dj_rest_auth.views import LoginView, LogoutView
from django.contrib.auth.views import LoginView
from django_otp.forms import OTPAuthenticationForm
from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

class OTPAdmin(OTPAdminSite):
    pass

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)

urlpatterns = [
    path('mfa/', LoginView.as_view(authentication_form=OTPAuthenticationForm)),
    path('', login.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('tw_admin/', admin_site.urls),
    path('bankapp/', include('BankApp.urls')),
    path('user/', include('rest_framework.urls', namespace='user')),
    path('bankapp/dj-rest-auth/', include('dj_rest_auth.urls')), 
    path('bankapp/dj-rest-auth/registration', include('dj_rest_auth.registration.urls')),
]
