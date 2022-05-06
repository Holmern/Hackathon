from django.urls import path
from .api import index, customer_page, transaction_action, account_details, create_customer, employeeindex

app_name = 'BankApp'

urlpatterns = [
    path('', index.as_view()),
    path('employeeindex', employeeindex.as_view(), name='employeeindex'),
    path('details/<int:pk>', customer_page.as_view(), name='customer_page'),
    path('accountdetails/<int:pk>', account_details.as_view(), name='account_details'),
    path('createcostumer', create_customer.as_view(), name='create_accounts'),
    #path('transfer', fronttransfer.as_view(), name='transfer'),
    path('transactionaction', transaction_action.as_view(), name='transaction_action'),
]
