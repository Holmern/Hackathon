from django.contrib import admin
from .models import Customer, Account, Bank, Employee, Ledger

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Bank)
admin.site.register(Employee)
admin.site.register(Ledger)