from decimal import Decimal
from email.mime import application
import json
from secrets import token_urlsafe

import requests
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth_func import create_OTP
from .models import Account, Customer, Ledger
from .serializers import *


class login(APIView):
    permissions_classes = [permissions.IsAuthenticated, ]
    permissions_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('/bankapp/staff_dashboard')
            else:
                return redirect('/bankapp/dashboard')
        else:    
            return redirect('/mfa/')


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

        queryset = Account.objects.filter(user=request.user, pk=pk)
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'account': account_data})


class transaction_details(generics.RetrieveDestroyAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/transaction_details.html'
    serializer_class = AccountSerializer
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

            transfer = Ledger.transfer(int(amount), debit_account, debit_text, credit_account, credit_text)
            return redirect(f'/bankapp/transaction_details/{transfer}')
    
    def get(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        queryset = request.user.customer.accounts
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'accounts': account_data})

class make_external_transfer(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/make_external_transfer.html'
    serializer_class = TransferExternalSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    
    def post(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'
        serializer = TransferExternalSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            amount = request.data['amount']
            debit_account = Account.objects.filter(pk=request.data['debit_account']).first()
            debit_account_pk = request.data['debit_account']
            debit_text = request.data['debit_text']
            credit_account = Account.objects.filter(pk=request.data['credit_account']).first()
            credit_account_pk = request.data['credit_account']
            credit_text = request.data['credit_text']
            external_transfer = request.data['external_transfer']
            bank_code = request.data['bank_code']

            if bank_code == '8000':
                transfer = Ledger.extern_receive_transfer(int(amount), debit_account, debit_text, credit_account, f'External transfer: {credit_text}')
                return redirect(f'/bankapp/transaction_details/{transfer}') 
            elif bank_code == '5050':
                    
                transfer = Ledger.extern_transfer(int(amount), debit_account, f'External transfer: {debit_text}', credit_account, credit_text)
                    
                payload = {"amount": int(amount), "debit_account": debit_account_pk, "debit_text": debit_text, "credit_account": credit_account_pk,"credit_text": credit_text, "external_transfer": external_transfer, 'bank_code': bank_code}
                headers = {"Authorization": f'Token 99f0f6983d8e284f4cf7b03ac21e921e94953904'}#, "X-CSRFToken": request.data['csrfmiddlewaretoken']}
                r = requests.post(f'http://127.0.0.1:{bank_code}/bankapp/make_external_transfer/', data=payload, headers=headers)
                print(r.status_code, r)
                
                return redirect(f'/bankapp/transaction_details/{transfer}')
            else:
                return 'Wrong bank code' 
        else:
            print('serializer not valid!')
    
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
            return redirect('/bankapp/dashboard')

        if serializer.is_valid():
            request.user.customer.make_loan(Decimal(request.data['amount']), request.data['name'])
            return redirect('/bankapp/dashboard')

    def get(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        return Response({})


class user_details(generics.RetrieveUpdateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/user_details.html'
    serializer_class = CurrentUserSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    queryset = User.objects.all()
    lookup_field = 'pk'

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
            Q(user__username__contains=search_term)   |
            Q(user__first_name__contains=search_term) |
            Q(user__last_name__contains=search_term)  |
            Q(user__email__contains=search_term)      |
            Q(personal_id__contains=search_term)    |
            Q(phone__contains=search_term)
        )[:15]
        customers_data = CustomerSerializer(customers, many=True).data
        return Response({'customers': customers_data})

class staff_customer_details(generics.RetrieveUpdateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_customer_details.html'
    serializer_class = CustomerSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    queryset = Customer.objects.all()
    
    def get(self, request, pk):
        assert request.user.is_staff, 'Customer user routing staff view.'

        customer = Customer.objects.filter(pk=pk)
        customer_data = CustomerSerializer(customer, many=True).data
        return Response({'customer': customer_data})

class staff_account_list_partial(generics.ListAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_account_list_partial.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        assert request.user.is_staff, 'Customer user routing staff view.'

        customer = Customer.objects.filter(pk=pk).first()
        user=User.objects.get(pk=customer.user.pk)
        print(customer)
        accounts = Account.objects.filter(user=user)
        account_data = AccountSerializer(accounts, many=True).data
        print(account_data)
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
    serializer_class = NewAccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def post(self, request, user):
        assert request.user.is_staff, 'Customer user routing staff view.'
        serializer = NewAccountSerializer(data=request.data)

        if serializer.is_valid():
            customer = Customer.objects.filter(pk=user).first()
            Account.objects.create(user=User.objects.get(pk=customer.user.pk), name=request.data['new_account'])
        return redirect(f'/bankapp/staff_customer_details/{user}')


class staff_new_customer(generics.CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_new_customer.html'
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
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            print(f'** Username: {username} -- Password: {password}')
            print(f'user: {user}  -- rank: {rank}  -- personal: {personal_id}  -- phone {phone} ')
            customer = Customer.objects.create(user=user, rank=rank, personal_id=personal_id, phone=phone)
            Token.objects.create(user=user)
            create_OTP(user, password)
            return redirect(f'/bankapp/staff_customer_details/{customer.pk}')
        else:
            return Response(serializer.data)

class convert_currency(generics.ListAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/currency_convert.html'
    serializer_class = ConvertSerializer
    permissions_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        return Response({})

    def post(self, request):
        serializer = ConvertSerializer(data = request.data)
        if serializer.is_valid():
            # Where USD is the base currency you want to use
            currency1 = request.data['currency1']
            amount = request.data['amount']
            currency2 = request.data['currency2']
            url = f'https://v6.exchangerate-api.com/v6/e19f110df09288776f9cbd42/latest/{currency1}'

            # Making our request
            response = requests.get(url)
            data = response.json()
            con_rate = data["conversion_rates"]
            con_rate = con_rate[currency2]
            amount2 = round((float(amount) * con_rate),2)
            ResultCurrency = f'{currency2} {amount2}'

            # Your JSON object
            print(amount2)
            print(con_rate)
            return Response({'amount':ResultCurrency})
