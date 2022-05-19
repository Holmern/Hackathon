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
from .models import Account, Ledger, Customer, UID
from .errors import InsufficientFunds
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.db.models import Q
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

#REST - DONE
class index(APIView):
    permissions_classes = [permissions.IsAuthenticated, ]
    #permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_staff:
            return redirect('/bankapp/staff_dashboard')
        else:
            return redirect('/bankapp/dashboard')

        
'''@login_required
def index(request):
    if request.user.is_staff:
        #return HttpResponseRedirect(reverse('BankApp:staff_dashboard'))
        #Command.handle(self)
        return redirect('/bankapp/staff_dashboard')
    else:
        #return HttpResponseRedirect(reverse('BankApp:dashboard'))
        return redirect('/bankapp/dashboard')'''

# REST - DONE
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

'''@login_required
def dashboard(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    accounts = request.user.customer.accounts
    context = {
        'accounts': accounts,
    }
    return render(request, 'BankApp/dashboard.html', context)'''

# REST - DONE
class account_details(generics.RetrieveDestroyAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/account_details.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    
    def get(self, request, pk):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        #queryset = get_object_or_404(Account, user=request.user, pk=pk)
        queryset = Account.objects.filter(user=request.user, pk=pk)
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'account': account_data})


'''@login_required
def account_details(request, pk):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    account = get_object_or_404(Account, user=request.user, pk=pk)
    context = {
        'account': account,
    }
    return render(request, 'BankApp/account_details.html', context)'''


'''@login_required
def transaction_details(request, transaction):
    movements = Ledger.objects.filter(transaction=transaction)
    if not request.user.is_staff:
        if not movements.filter(account__in=request.user.customer.accounts):
            raise PermissionDenied('Customer is not part of the transaction.')
    context = {
        'movements': movements,
    }
    return render(request, 'BankApp/transaction_details.html', context)'''

# REST - DONE
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
        movements_data = LedgerSerializer(queryset, many=True).data
        return Response({'movements': movements_data})

'''@login_required
def make_transfer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    if request.method == 'POST':
        form = TransferForm(request.POST)
        form.fields['debit_account'].queryset = request.user.customer.accounts
        if form.is_valid():
            amount = form.cleaned_data['amount']
            debit_account = Account.objects.get(pk=form.cleaned_data['debit_account'].pk)
            debit_text = form.cleaned_data['debit_text']
            credit_account = Account.objects.get(pk=form.cleaned_data['credit_account'])
            credit_text = form.cleaned_data['credit_text']
            try:
                transfer = Ledger.transfer(amount, debit_account, debit_text, credit_account, credit_text)
                return transaction_details(request, transfer)
            except InsufficientFunds:
                context = {
                    'title': 'Transfer Error',
                    'error': 'Insufficient funds for transfer.'
                }
                return render(request, 'BankApp/error.html', context)
    else:
        form = TransferForm()
    form.fields['debit_account'].queryset = request.user.customer.accounts
    context = {
        'form': form,
    }
    return render(request, 'BankApp/make_transfer.html', context)'''

# Cannot assign "<bound method ? of <class 'BankApp.models.UID'>>": "Ledger.transaction" must be a "UID" instance.
class make_transfer(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/make_transfer.html'
    serializer_class = TransferSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        data = request.POST
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = request.POST['amount']
            debit_account = Account.objects.get(pk=request.POST['debit_account'])
            debit_text = request.POST['debit_text']
            credit_account = Account.objects.get(pk=request.POST['credit_account'])
            credit_text = request.POST['credit_text']
            try:
                #transfer = Ledger.transfer(int(amount), debit_account, debit_text, credit_account, credit_text)
                if debit_account.balance >= float(amount):
                #uid = UID.uid
                #cls(amount=-amount, transaction=uid, account=debit_account, text=debit_text).save()
                #cls(amount=amount, transaction=uid, account=credit_account, text=credit_text).save()
                    Ledger.objects.create(amount=float(amount), transaction=UID.uid, account=debit_account, text=debit_text).save()
                    Ledger.objects.create(amount=float(amount), transaction=UID.uid, account=credit_account, text=credit_text).save()
                else:
                    raise InsufficientFunds


                transfer = Ledger.transfer(int(amount), debit_account, debit_text, credit_account, credit_text)
                return redirect(f'/bankapp/transaction_details/{transfer}')
            except InsufficientFunds:
                context = {
                    'title': 'Transfer Error',
                    'error': 'Insufficient funds for transfer.'
                }                
                return Response({'error':context}) #<-- Dette driller øv.. Ingen error info kommer tilbage..
        
    def get(self, request):
        assert not request.user.is_staff, 'Staff user routing customer view.'

        queryset = request.user.customer.accounts
        account_data = AccountSerializer(queryset, many=True).data
        return Response({'accounts': account_data})


# Cannot assign "<bound method ? of <class 'BankApp.models.UID'>>": "Ledger.transaction" must be a "UID" instance.
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

'''
@login_required
def make_loan(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    if not request.user.customer.can_make_loan:
        context = {
            'title': 'Create Loan Error',
            'error': 'Loan could not be completed.'
        }
        return render(request, 'BankApp/error.html', context)
    if request.method == 'POST':
        request.user.customer.make_loan(Decimal(request.POST['amount']), request.POST['name'])
        return redirect('/bankapp/dashboard')
    return render(request, 'BankApp/make_loan.html', {})
'''

# Staff views

'''@login_required
def staff_dashboard(request):
    assert request.user.is_staff, 'Customer user routing staff view.'

    return render(request, 'BankApp/staff_dashboard.html')'''

# REST - DONE
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
            Q(personal_id__contains=search_term)      |
            Q(phone__contains=search_term)
        )[:15]
        customers_data = CustomerSerializer(customers, many=True).data
        print(customers_data)
        return Response({'customers': customers_data})

'''
class staff_customer_details(generics.RetrieveUpdateAPIView):
    #renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    #template_name = 'BankApp/staff_customer_details.html'
    serializer_class = CustomerSerializer
    permissions_classes = [permissions.IsAuthenticated, ]
    queryset = Customer

    def get(self, request, pk):
        assert request.user.is_staff, 'Customer user routing staff view.'

        customer = Customer.objects.filter(pk=pk)
        accounts = customer.accounts
        account_data = AccountSerializer(accounts, many=True).data
        return Response({'accounts': account_data})
'''

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

'''
@login_required
def staff_account_list_partial(request, pk):
    assert request.user.is_staff, 'Customer user routing staff view.'

    customer = Customer.objects.filter(pk=pk)
    print()
    accounts = customer.accounts
    account_data = AccountSerializer(accounts, many=True).data
    return Response({'accounts': account_data})
'''

class staff_account_list_partial(generics.ListAPIView): # <--- TEST!
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_account_list_partial.html'
    serializer_class = AccountSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def get(self, request, pk):
        assert request.user.is_staff, 'Customer user routing staff view.'

        customer = Customer.objects.filter(pk=pk)
        print(customer.user)
        #accounts = customer.accounts
        account_data = AccountSerializer(accounts, many=True).data
        return Response({'accounts': account_data})
    

'''@login_required
def staff_account_details(request, pk):
    assert request.user.is_staff, 'Customer user routing staff view.'

    account = get_object_or_404(Account, pk=pk)
    context = {
        'account': account,
    }
    return render(request, 'BankApp/account_details.html', context)'''

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
        return Response({'account': account})

'''
@login_required
def staff_new_account_partial(request, user):
    assert request.user.is_staff, 'Customer user routing staff view.'

    if request.method == 'POST':
        new_account_form = NewAccountForm(request.POST)
        if new_account_form.is_valid():
            Account.objects.create(user=User.objects.get(pk=user), name=new_account_form.cleaned_data['name'])
    #return HttpResponseRedirect(reverse('BankApp:staff_customer_details', args=(user,)))
    return redirect(f'/bankapp/staff_customer_details/{user}')
'''

# REST - DONE
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
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/staff_new_account_partial.html'
    serializer_class = CustomerSerializer
    permissions_classes = [permissions.IsAuthenticated, ]

    def post(self, request, user):
        assert request.user.is_staff, 'Customer user routing staff view.'

        ser



@login_required
def staff_new_customer(request):
    assert request.user.is_staff, 'Customer user routing staff view.'

    if request.method == 'POST':
        new_user_form = NewUserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if new_user_form.is_valid() and customer_form.is_valid():
            username    = new_user_form.cleaned_data['username']
            first_name  = new_user_form.cleaned_data['first_name']
            last_name   = new_user_form.cleaned_data['last_name']
            email       = new_user_form.cleaned_data['email']
            password    = token_urlsafe(8)
            rank        = customer_form.cleaned_data['rank']
            personal_id = customer_form.cleaned_data['personal_id']
            phone       = customer_form.cleaned_data['phone']
            try:
                user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                )
                print(f'********** Username: {username} -- Password: {password}')
                Customer.objects.create(user=user, rank=rank, personal_id=personal_id, phone=phone)
                create_OTP(user)
                return staff_customer_details(request, user.pk)
            except IntegrityError:
                context = {
                    'title': 'Database Error',
                    'error': 'User could not be created.'
                }
                return render(request, 'BankApp/error.html', context)
    else:
        new_user_form = NewUserForm()
        customer_form = CustomerForm()
    context = {
        'new_user_form': new_user_form,
        'customer_form': customer_form,
    }
    return render(request, 'BankApp/staff_new_customer.html', context)

# Func for 2-way-Auth
def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
# Func for 2-way-Auth
def create_OTP(user):
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=True)
    url = device.config_url
    #print(url)
    url = url.split('=')
    qr_code_url = url[1].replace('&algorithm', '')
    print(f'********* QR-Code: {qr_code_url} *********')
    return qr_code_url