from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Customer, Account, Bank, Employee, Ledger, CreateTransaction, CompleteTransaction
# from .calls import CreateTransaction, CompleteTransaction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # IF it is a customer who is logging in
    if (Customer.objects.filter(user=request.user).first()) is not None:
        Cus = Customer.objects.get(user=request.user).id
        Accounts = Account.objects.filter(customer_id=Cus)
        print(Accounts)
        context = {
            'Accounts': Accounts
        }
        return render(request, 'BankApp/index.html', context)
    
    # IF it is a employee who is logging in
    elif (Employee.objects.filter(user=request.user).first()) is not None:
            Bank = Employee.objects.get(user=request.user).bank_id
            search = request.GET.get('search')
            print(search)
            Bank = Employee.objects.get(user=request.user).bank_id
            Customers = Customer.objects.filter(bank_id=Bank)
            context = {
                'Customers': Customers,
                'Bank': Bank
            }
            return render(request, 'BankApp/employeeindex.html', context)

@login_required
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

# Define function to display the particular book

@login_required
def customer_page(request,id):
    customer = Customer.objects.get(id=id)
    Accounts = Account.objects.filter(customer_id=customer.id)
    print(Accounts)
    return render(request, 'BankApp/customerpage.html', {'customer': customer, 'accounts': Accounts})


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
