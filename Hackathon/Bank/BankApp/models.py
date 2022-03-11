from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import date

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


RANK_TYPES = (
    ("Basis", "Basis"),
    ("Silver", "Silver"),
    ("Gold", "Gold")
)


class Customer(models.Model):
    First_name = models.CharField(max_length=20)
    Last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField(max_length = 100)
    rank = models.CharField(max_length=11, choices = RANK_TYPES)
    bank_id = models.ForeignKey(Bank, on_delete = models.CASCADE, default = None)


class User(AbstractUser, models.Model):   
    kind_of_user =  models.CharField(max_length=20)
    user_fk = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_fk', 'kind_of_user']
    
    def __str__(self):
        return "{}".format(self.username_fk)


class Employee(models.Model):
    First_name = models.CharField(max_length=20)
    Last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    email = models.EmailField(max_length = 100)
    bank_id = models.ForeignKey(Bank, on_delete = models.CASCADE, default = None)


ACCOUNT_TYPES = (
    ("Checkings", "Checkings"),
    ("savings", "Savings"),
    ("Loans", "Loans")
)


class Account(models.Model):
    amount = models.FloatField()
    name = models.CharField(max_length=40)
    account_type = models.CharField(max_length=11, choices = ACCOUNT_TYPES)
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE, default = None)
    bank_id = models.ForeignKey(Bank, on_delete = models.CASCADE, default = None)


class Transaction(models.Model):
    description = models.CharField(max_length=40)
    amount = models.FloatField()
    from_account_id = models.IntegerField()
    to_account_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.ForeignKey(Customer, on_delete = models.CASCADE, default = None)




