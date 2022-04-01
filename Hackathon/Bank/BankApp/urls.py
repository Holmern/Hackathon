from django.urls import path
from . import views

app_name = 'BankApp'

urlpatterns = [
    path('', views.index, name='index'),
    path('employeeindex', views.index, name='employeeindex'),
    path('details/<id>', views.customer_page, name='customer_page'),
    path('customerupdate/<id>', views.customerupdate, name='customer_update'),
    path('deactivate/<id>', views.deactivate_user, name='deactivate_user'),
    #path('search', views.search, name='search'),
    path('transfer', views.fronttransfer, name='transfer'),
    path('transactionaction', views.transaction_action, name='transaction_action'),
]
