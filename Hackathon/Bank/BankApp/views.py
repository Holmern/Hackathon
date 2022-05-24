from decimal import Decimal
from secrets import token_urlsafe
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from .forms import TransferForm, UserForm, CustomerForm, NewUserForm, NewAccountForm
from .models import Account, Ledger, Customer
from .errors import InsufficientFunds
from .serializers import *
from .auth_func import create_OTP
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.db.models import Q

class index(APIView):
    permissions_classes = [permissions.IsAuthenticated, ]
    #permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_staff:
            return redirect('/bankapp/staff_dashboard')
        else:
            return redirect('/bankapp/dashboard')


# Customer views
class dashboard(generics.ListAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/dashboard.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        queryset = request.user.customer.accounts
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'accounts': account_data})


class account_details(generics.RetrieveDestroyAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/account_details.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    
    def get(self, request, pk):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        queryset = get_object_or_404(Account, user=request.user, pk=pk)
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'account': account_data})


class transaction_details(generics.RetrieveDestroyAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/transaction_details.html'
    serializer_class = AccountSerializer # <---
    permissions_classes = [permissions.IsAuthenticated, ]
    
    def get(self, request, transaction):
        queryset = Ledger.objects.filter(transaction=transaction)
        if not request.user.is_staff:
            if not queryset.filter(account__in=request.user.customer.accounts):
                raise PermissionDenied('Customer is not part of the transaction.')
        movement_data = LedgerSerializer(queryset, many=True).data
        return Response({'movements': movement_data})


class make_transfer(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/make_transfer.html'
    serializer_class = TransferSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = request.POST['amount']
            debit_account = Account.objects.get(pk=request.POST['debit_account'])
            debit_text = request.POST['debit_text']
            credit_account = Account.objects.get(pk=request.POST['credit_account'])
            credit_text = request.POST['credit_text']
            #--------------------#
            try:
                transfer = Ledger.transfer(amount, debit_account, debit_text, credit_account, credit_text)
                return redirect(f'/bankapp/transaction_details/{transfer}')
            except InsufficientFunds:
                context = {
                    'title': 'Transfer Error',
                    'error': 'Insufficient funds for transfer.'
                }
                error = errorSerializer(context, many=True).data                
                return Response({'error':error}) #<-- Dette driller øv.. Ingen error info kommer tilbage..
    
    def get(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        queryset = request.user.customer.accounts
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'accounts': account_data})

class make_loan(generics.CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/make_loan.html'
    serializer_class = LoanSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        serializer = LoanSerializer(data=request.data)

        if not request.user.customer.can_make_loan:
            context = {
                'title': 'Create Loan Error',
                'error': 'Loan could not be completed.'
            }
            return redirect('/bankapp/dashboard') # clean up - return error

        if serializer.is_valid():
            request.user.customer.make_loan(Decimal(request.POST['amount']), request.POST['name'])
            return redirect('/bankapp/dashboard')

    def get(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        return Response({})


# Staff views

class staff_dashboard(generics.ListAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_dashboard.html'
    serializer_class = SearchSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        assert request.user.is_staff, 'Customer user routing staff view.'
        return Response({})

    def post(self, request):
        assert request.user.is_staff, 'Customer user routing staff view.'

        search_term = request.POST['search_term']
        customers = Customer.objects.filter(
            Q(userusernamecontains=search_term)   |
            Q(userfirst_namecontains=search_term) |
            Q(userlast_namecontains=search_term)  |
            Q(useremailcontains=search_term)      |
            Q(personal_idcontains=search_term)    |
            Q(phonecontains=search_term)
        )[:15]
        customers_data = CustomerSerializer(customers, many=True).data
        print(customers_data)
        return Response({'customers': customers_data})
   

@login_required
def staff_customer_details(request, pk):
    assert request.user.is_staff, 'Customer user routing staff view.'

    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'GET':
        user_form = UserForm(instance=customer.user)
        customer_form = CustomerForm(instance=customer)
    elif request.method == 'POST':
        user_form = UserForm(request.POST, instance=customer.user)
        customer_form = CustomerForm(request.POST, instance=customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
    new_account_form = NewAccountForm()
    context = {
        'customer': customer,
        'user_form': user_form,
        'customer_form': customer_form,
        'new_account_form': new_account_form,
    }
    return render(request, 'BankApp/staff_customer_details.html', context)


class staff_account_list_partial(generics.ListAPIView): # <--- TEST!
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_account_list_partial.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        assert request.user.is_staff, 'Customer user routing staff view.'

        customer = Customer.objects.filter(pk=pk)
        print(customer.user)
        accounts = customer.accounts #<--- test
        account_data = AccountSerializer(accounts, many=True).data
        return Response({'accounts': account_data})

# REST - DONE
class staff_account_details(generics.ListAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/account_details.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        assert request.user.is_staff, 'Customer user routing staff view.'

        account = Account.objects.filter(pk=pk)
        account_data = AccountSerializer(account, many=True).data
        return Response({'account': account_data})


class staff_new_account_partial(generics.CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_new_account_partial.html'
    serializer_class = NewAccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def post(self, request, user):
        assert request.user.is_staff, 'Customer user routing staff view.'
        serializer = NewAccountSerializer(data=request.data)

        if serializer.is_valid():
            Account.objects.create(user=User.objects.get(pk=user), name=request.POST['name'])
        return redirect(f'/bankapp/staff_customer_details/{user}')


class staff_new_customer(generics.CreateAPIView):
    #renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    #template_name = 'BankApp/staff_new_customer.html'
    serializer_class = NewUserCustomerSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        assert request.user.is_staff, 'Customer user routing staff view.'
        return Response({})

    def post(self, request):
        assert request.user.is_staff, 'Customer user routing staff view.'

        serializer = NewUserCustomerSerializer(data=request.data)
        if serializer.is_valid():
            username    = request.data['username']
            first_name  = request.data['first_name']
            last_name   = request.data['last_name']
            email       = request.data['email']
            password    = token_urlsafe(8)
            rank        = request.data['rank']
            personal_id = request.data['personal_id']
            phone       = request.data['phone']
            print(f'-- rank: {rank}  -- personal: {personal_id}  -- phone {phone} ')
            #rank1 = Rank.objects.filter(pk=rank).first()
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            print(f'** Username: {username} -- Password: {password}')
            print(f'user: {user}  -- rank: {rank}  -- personal: {personal_id}  -- phone {phone} ')
            Customer.objects.create(user=user, rank=rank, personal_id=personal_id, phone=phone)
            create_OTP(user, password)
            return redirect(f'/bankapp/staff_customer_details/{user.pk}')
        else:
            context = {
                'error': "error was made"
            }
            return Response(serializer.data)