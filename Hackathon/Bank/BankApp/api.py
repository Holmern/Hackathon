from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .models import Customer, Account, Bank, Employee, Ledger, CreateTransaction, CompleteTransaction
# from .calls import CreateTransaction, CompleteTransaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Bank, Customer, Employee, Account, Ledger
from .serializers import *

class index(generics.ListCreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'BankApp/index.html'
    serializer_class = AccountSerializer
    permissions_classes = (permissions.IsAuthenticated)

    def get(self, request):
        # IF it is a customer who is logging in
        if (Customer.objects.filter(user=self.request.user).first()) is not None:
            Cus = Customer.objects.get(user=self.request.user).id
            queryset = Account.objects.filter(customer_id=Cus)
            return Response({'Accounts': queryset})

class employeeindex(generics.ListCreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'BankApp/employeeindex.html'
    serializer_class = AccountSerializer
    permissions_classes = (permissions.IsAuthenticated)
    # IF it is a employee who is logging in
    def get(self, request):
        if (Employee.objects.filter(user=self.request.user).first()) is not None:
            Bank = Employee.objects.get(user=self.request.user).bank_id
            queryset = Customer.objects.filter(bank_id=Bank)
            return Response({'Customers': queryset})

# CREATE CUSTOMER AS EMPLOYEE
class create_customer(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'createcustomer.html' # EXISTERE IKKE ENDNU
        #queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permissions_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        if (Employee.objects.filter(user=self.request.user).first()) is not None:
            return Customer.objects.all()

# SEE/EDIT CUSTOMER AS EMPLOYEE
class customer_page(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customerpage.html'
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permissions_classes = (permissions.IsAuthenticated)

#SEE/EDIT ACCOUNTS AS EMPLOYEE
class account_details(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permissions_classes = (permissions.IsAuthenticated)


class transaction_action(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'transfer.html'
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