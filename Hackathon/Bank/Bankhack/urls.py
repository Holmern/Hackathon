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
from django.contrib.auth.views import LoginView
from django.urls import include, path
from django_otp.forms import OTPAuthenticationForm

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='3WHS API DOCS')
from django.urls import path

urlpatterns = [
    path('docs/', schema_view)
]  

urlpatterns += [
    path('mfa/', LoginView.as_view(authentication_form=OTPAuthenticationForm)),
    path('admin/', admin.site.urls),
    path('bankapp/', include('BankApp.urls')),
    path('user/', include('rest_framework.urls', namespace='user')),
    path('bankapp/dj-rest-auth/', include('dj_rest_auth.urls')), 
    path('bankapp/dj-rest-auth/registration', include('dj_rest_auth.registration.urls')),
]

