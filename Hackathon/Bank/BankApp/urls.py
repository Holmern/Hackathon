from django.urls import path
from . import views

app_name = 'BankApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('/transfer', views.fronttransfer, name='transfer'),
    path('/transactionaction', views.transaction_action, name='transaction_action'),
]
