from django.urls import path
from .views import index, customer_page, customerupdate, deactivate_user, fronttransfer, transaction_action, account_details

app_name = 'BankApp'

urlpatterns = [
    path('', index.as_view()),
    path('employeeindex', index.as_view(), name='employeeindex'),
    path('details/<int:pk>', customer_page.as_view(), name='customer_page'),
    path('accountdetails/<int:pk>', account_details.as_view(), name='account_details'),
    #path('customerupdate/<int:id>', customerupdate.as_view(), name='customer_update'),
    #path('deactivate/<int:id>', deactivate_user.as_view, name='deactivate_user'),
    #path('search', views.search, name='search'),
    #path('transfer', fronttransfer.as_view, name='transfer'),
    #path('transactionaction', transaction_action.as_view, name='transaction_action'),
]
