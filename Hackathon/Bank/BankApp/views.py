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

#@login_required
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

#@login_required
def customerupdate(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        rank = request.POST["rank"]
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.email = email
        customer.rank = rank
        customer.save()
    return render(request, 'BankApp/customerupdate.html', {'customer': customer})


@login_required
def deactivate_user(request, id):
    if request.method == "POST":
        try:
            user = Customer.objects.get(id=id).user
            user.is_active = False
            user.save()
            print('Profile successfully disabled.')
        except:
            print("failed")


#   VIRKER IKKE
def search(request):
    if request.GET.get('myform'):
        search = request.GET.get('search')
        print(search)
        Bank = Employee.objects.get(user=request.user).bank_id
        Customers = Customer.objects.filter(bank_id=Bank, phone=search)
        context = {
            'Customers': Customers
            }
        return render(request, 'BankApp/employeeindex.html', context)


    # ELSE User dont have a Login
    else:
        return render(request, 'login_app/login.html')


class customer_page(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class account_details(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@login_required
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


@login_required
def fronttransfer(request):
    return render(request, 'BankApp/transfer.html')
