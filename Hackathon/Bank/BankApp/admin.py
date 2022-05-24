from django.contrib import admin
from .models import Customer, Account, Ledger, UID

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Ledger)
admin.site.register(UID)


