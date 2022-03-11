from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Customer, Account, Bank, Employee, Transaction
from .calls import CreateTransaction, CompleteTransaction


def index(request):
    '''
    if request.method == "POST":
        text = request.POST["text"]
        todo = Todo()
        todo.user = request.user
        todo.text = text
        todo.save()
'''
    Customerr = Customer.objects.get(user=request.user).id
    Accounts = Account.objects.filter(customer_id=Customerr)
    print(Accounts)
    context = {
        'Accounts': Accounts
    }
    return render(request, 'BankApp/index.html', context)


def transaction_action(request):
    description = request.POST["description"]
    from_acc = request.POST["from_acc"]
    to_acc = request.POST["to_acc"]
    amount = request.POST["amount"]
    customer_id = Customer.objects.get(user=request.user).id

    from_account = Account.objects.get(id=from_acc, customer_id=customer_id)
    fromnew = amount - from_account.amount
    to_account = Account.objects.get(id=to_acc, customer_id=customer_id)
    tonew= amount + to_account.amount

    CreateTransaction(description, from_acc, to_acc, amount, customer_id)
    CompleteTransaction(from_acc, to_acc, amount, fromnew, tonew, customer_id)
    
    return HttpResponseRedirect(reverse('BankApp/index'))



def fronttransfer(request):
    return render(request, 'BankApp/transfer.html')
