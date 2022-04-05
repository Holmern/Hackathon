from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Customer, Account, Bank, Employee, Ledger, CreateTransaction, CompleteTransaction
# from .calls import CreateTransaction, CompleteTransaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Bank, Customer, Employee, Account, Ledger
from .serializers import *

# FRONT AS CUSTOMER AND EMPLOYEE
class index(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permissions_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        # IF it is a customer who is logging in
        if (Customer.objects.filter(user=self.request.user).first()) is not None:
            Cus = Customer.objects.get(user=self.request.user).id
            return Account.objects.filter(customer_id=Cus)
    
    # IF it is a employee who is logging in
        elif (Employee.objects.filter(user=self.request.user).first()) is not None:
            Bank = Employee.objects.get(user=self.request.user).bank_id
            search = self.request.GET.get('search')
            print(search)
            Bank = Employee.objects.get(user=self.request.user).bank_id
            return Customer.objects.filter(bank_id=Bank)

# CREATE CUSTOMER AS EMPLOYEE
class create_customer(generics.CreateAPIView):
        #queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permissions_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        if (Employee.objects.filter(user=self.request.user).first()) is not None:
            return Customer.objects.all()

# SEE/EDIT CUSTOMER AS EMPLOYEE
class customer_page(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permissions_classes = (permissions.IsAuthenticated)

#SEE/EDIT ACCOUNTS AS EMPLOYEE
class account_details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permissions_classes = (permissions.IsAuthenticated)





class transaction_action(generics.CreateAPIView):
    serializer_class = LedgerSerializer

    def post(self, request, *args, **kwargs):
        description = request.data["description"]
        amount = request.data["amount"]
        from_acc = request.data["from_acc"]
        to_acc = request.data["to_acc"]
        customer_id = Customer.objects.get(user=self.request.user)
        CreateTransaction(description, from_acc, to_acc, amount, customer_id)
        CompleteTransaction(from_acc, to_acc, amount, fromnew, tonew, customer_id)
        return self.create(request, *args, **kwargs)

        
'''
def transaction_action(request):
    description = request.POST["description"]
    amount = request.POST["amount"]
    from_acc = request.POST["from_acc"]
    to_acc = request.POST["to_acc"]
    customer_id = Customer.objects.get(user=request.user)

    if request.method == "POST":
        CreateTransaction(description, from_acc, to_acc, amount, customer_id)
        CompleteTransaction(from_acc, to_acc, amount, fromnew, tonew, customer_id)
    
    return HttpResponseRedirect(reverse('BankApp:index'))
'''


def fronttransfer(request):
    return render(request, 'BankApp/transfer.html')
