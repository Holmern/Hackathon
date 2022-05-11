from dataclasses import field
from rest_framework import serializers
from .models import Customer, Account, Ledger


'''class AccountSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'amount', 'name', 'account_type', 'customer_id', 'bank_id')
        model = Account'''

class AccountSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('user', 'name', 'movements', 'balance')
        model = Account


class CustomerSerializer (serializers.ModelSerializer):
    #account_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #account_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountdetails')

    class Meta:
        fields = ('user', 'rank', 'personal_id', 'phone', 'full_name', 'accounts', 'can_make_loan', 'default_account')
        model = Customer

class LedgerSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('account', 'transaction','amount', 'timestamp', 'text')
        model = Ledger

class TransferFormSerializer (serializers.Serializer):

    class Meta:
        fields = ('account', 'debit_account', 'debit_text', 'credit_account', 'credit_text')
        