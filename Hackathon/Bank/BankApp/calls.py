from .models import Transaction, Account, Customer, Bank
from django.db import IntegrityError


def CreateTransaction(description, from_acc, to_acc, amount, customer_id):

    transaction = Transaction()
    # id = uuid.uuid4()  # import
    Transaction(
        description=description,
        amount=float(amount),
        t_type="CREDIT",
        account_id=to_acc,
        #customer_id=customer_id
    )
    transaction.customer_id = customer_id
    transaction.save()
    Transaction(
        description=description,
        amount=float(amount),
        t_type="DEBIT",
        account_id=from_acc,
        customer_id=customer_id
    )
    transaction.customer_id = customer_id
    transaction.save()


def CompleteTransaction(from_acc, to_acc, amount, fromnew, tonew, customer_id):
    account = Account()
    #from_account = Account.objects.get(id=from_acc, customer_id=customer_id)
    account.customer_id = Customer.objects.get(id=customer_id)
    customer = Customer.objects.get(id=customer_id)
    bank = Bank.objects.get(id=customer.bank_id)
    account.bank_id = bank.id
    Account.objects.filter(id=from_acc).update(amount=fromnew)
    account.save()
    # to_account = Account.objects.get(id=to_acc)
    Account.objects.filter(id=to_acc).update(amount=tonew)
    account.save()
