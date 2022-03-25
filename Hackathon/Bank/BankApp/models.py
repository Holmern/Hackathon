from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import date

# Create your models here.
class Bank(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return '{} {}'.format(self.name, self.address)


RANK_TYPES = (
    ("Basis", "Basis"),
    ("Silver", "Silver"),
    ("Gold", "Gold")
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField(max_length = 100)
    rank = models.CharField(max_length=11, choices = RANK_TYPES)
    bank_id = models.ForeignKey(Bank, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.id, self.first_name, self.last_name, self.phone, self.email, self.rank, self.bank_id)

'''
class User(AbstractUser, models.Model):   
    kind_of_user =  models.CharField(max_length=20)
    user_fk = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_fk', 'kind_of_user']
    
    def __str__(self):
        return "{}".format(self.username_fk)
'''

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField(max_length = 100)
    bank_id = models.ForeignKey(Bank, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.first_name, self.last_name, self.phone, self.email, self.bank_id)


ACCOUNT_TYPES = (
    ("Checkings", "Checkings"),
    ("savings", "Savings"),
    ("Loans", "Loans")
)


class Account(models.Model):
    amount = models.FloatField(null=True)
    name = models.CharField(max_length=40)
    account_type = models.CharField(max_length=11, choices = ACCOUNT_TYPES)
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE, default = None)
    bank_id = models.ForeignKey(Bank, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.amount, self.name, self.account_type, self.customer_id, self.bank_id)


class Transaction(models.Model):
    description = models.CharField(max_length=40)
    amount = models.FloatField(null=True)
    t_type = models.CharField(max_length=40)
    account_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.description, self.amount, self.account_id, self.t_type, self.timestamp, self.customer_id)


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
