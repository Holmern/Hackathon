from django.urls import path
from .views import index, dashboard, account_details, transaction_details, make_transfer, staff_dashboard, staff_customer_details, staff_account_list_partial, staff_account_details, make_loan, staff_new_account_partial, staff_new_customer
from . import views


app_name = "bank"

urlpatterns = [
    #path('', views.index, name='index'),
    path('', index.as_view(), name='index'),

    #path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/', dashboard.as_view(), name='dashboard'),

    #path('account_details/<int:pk>/', views.account_details, name='account_details'),
    path('account_details/<int:pk>/', account_details.as_view(), name='account_details'),
    #path('transaction_details/<int:transaction>/', views.transaction_details, name='transaction_details'),
    path('transaction_details/<int:transaction>/', transaction_details.as_view(), name='transaction_details'),
    #path('make_transfer/', views.make_transfer, name='make_transfer'),
    path('make_transfer/', make_transfer.as_view(), name='make_transfer'),
    #path('make_loan/', views.make_loan, name='make_loan'),
    path('make_loan/', make_loan.as_view(), name='make_loan'),


    #path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_dashboard/', staff_dashboard.as_view(), name='staff_dashboard'),
    path('staff_customer_details/<int:pk>/', views.staff_customer_details, name='staff_customer_details'),
    #path('staff_customer_details/<int:pk>/', staff_customer_details.as_view(), name='staff_customer_details'),
    #path('staff_account_list_partial/<int:pk>/', views.staff_account_list_partial, name='staff_account_list_partial'),
    path('staff_account_list_partial/<int:pk>/', staff_account_list_partial.as_view(), name='staff_account_list_partial'),
    #path('staff_account_details/<int:pk>/', views.staff_account_details, name='staff_account_details'),
    path('staff_account_details/<int:pk>/', staff_account_details.as_view(), name='staff_account_details'),
    #path('staff_new_account_partial/<int:user>/', views.staff_new_account_partial, name='staff_new_account_partial'),
    path('staff_new_account_partial/<int:user>/', staff_new_account_partial.as_view(), name='staff_new_account_partial'),
    #path('staff_new_customer/', views.staff_new_customer, name='staff_new_customer'),
    path('staff_new_customer/', staff_new_customer.as_view(), name='staff_new_customer'),
]
