from rest_framework import serializers
from .models import Bank, Customer, Employee, Account, Ledger

class BankSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'address',)
        model = Bank


class AccountSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'amount', 'name', 'account_type', 'customer_id', 'bank_id')
        model = Account


class CustomerSerializer (serializers.ModelSerializer):
    account_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #account_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountdetails')

    class Meta:
        fields = ('id', 'user', 'first_name', 'last_name', 'phone', 'email', 'rank', 'bank_id', 'account_set')
        model = Customer

class EmployeeSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'user', 'first_name', 'last_name', 'phone', 'email', 'bank_id')
        model = Employee

class LedgerSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'description', 'amount', 't_type', 'amount_id', 'timestamp', 'customer_id', 'transaction')
        model = Ledger