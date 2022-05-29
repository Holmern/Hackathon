from django.urls import path
from . import views
from django.urls import re_path
from .views import (account_details, convert_currency, dashboard,
                    make_loan, make_transfer, staff_account_details,
                    staff_account_list_partial, staff_dashboard,
                    staff_new_account_partial, staff_new_customer,
                    transaction_details, login, staff_customer_details, user_details, make_external_transfer)

app_name = "bank"

urlpatterns = [
    path('', login.as_view(), name='login'),    

    #path('', index.as_view(), name='index'),
    path('dashboard/', dashboard.as_view(), name='dashboard'),
    path('account_details/<int:pk>/', account_details.as_view(), name='account_details'),
    path('transaction_details/<int:transaction>/', transaction_details.as_view(), name='transaction_details'),
    path('make_transfer/', make_transfer.as_view(), name='make_transfer'),
    path('make_external_transfer/', make_external_transfer.as_view(), name='make_external_transfer'),
    path('make_loan/', make_loan.as_view(), name='make_loan'),
    path('user_details/<int:pk>/', user_details.as_view(), name='user_details'),
    path('staff_dashboard/', staff_dashboard.as_view(), name='staff_dashboard'),
    #path('staff_customer_details/<int:pk>/', views.staff_customer_details, name='staff_customer_details'), #<-- Make as_view()!
    path('staff_customer_details/<int:pk>/', staff_customer_details.as_view(), name='staff_customer_details'),
    #path('staff_user_details/<int:pk>/', staff_user_details.as_view(), name='staff_user_details'),
    path('staff_account_list_partial/<int:pk>/', staff_account_list_partial.as_view(), name='staff_account_list_partial'),
    path('staff_account_details/<int:pk>/', staff_account_details.as_view(), name='staff_account_details'),
    path('staff_new_account_partial/<int:user>/', staff_new_account_partial.as_view(), name='staff_new_account_partial'),
    path('staff_new_customer/', staff_new_customer.as_view(), name='staff_new_customer'),
    path('convert_currency/', convert_currency.as_view(), name='convert_currency'),
]

