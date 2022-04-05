from django.urls import path
from .views import index, customer_page, fronttransfer, transaction_action, account_details, create_customer

app_name = 'BankApp'

urlpatterns = [
    path('', index.as_view()),
    path('employeeindex', index.as_view(), name='employeeindex'),
    path('details/<int:pk>', customer_page.as_view(), name='customer_page'),
    path('accountdetails/<int:pk>', account_details.as_view(), name='account_details'),
    path('createcostumer', create_customer.as_view(), name='create_accounts'),
    #path('transfer', fronttransfer.as_view(), name='transfer'),
    path('transactionaction', transaction_action.as_view(), name='transaction_action'),
]
