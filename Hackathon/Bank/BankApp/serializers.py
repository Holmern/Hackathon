from dataclasses import field
from rest_framework import serializers
from .models import Customer, Account, Ledger, UID
from drf_braces.serializers.form_serializer import FormSerializer
from .forms import TransferForm

'''class AccountSerializer (serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'amount', 'name', 'account_type', 'customer_id', 'bank_id')
        model = Account'''
class uidserializer (serializers.ModelSerializer):
    class Meta:
        model = UID
        fields = '__all__'


class LedgerSerializer (serializers.ModelSerializer):

    class Meta:
        #fields = ('account', 'transaction','amount', 'timestamp', 'text')
        model = Ledger
        fields = '__all__'



class AccountSerializer (serializers.ModelSerializer):
    movements = LedgerSerializer(many=True)

    class Meta:
        fields = ('pk', 'user', 'name', 'movements', 'balance')
        model = Account


class CustomerSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    accounts = AccountSerializer(many=True )
    #account_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #account_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='accountdetails')

    class Meta:
        fields = ('user', 'rank', 'personal_id', 'phone', 'full_name', 'accounts', 'can_make_loan', 'default_account')
        model = Customer


class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    debit_account = serializers.PrimaryKeyRelatedField(label='Debit Account', queryset=Account.objects.all())
    debit_text = serializers.CharField(label='Debit Account Text', max_length=25)
    credit_account = serializers.IntegerField(label='Credit Account Number')
    credit_text = serializers.CharField(label='Credit Account Text', max_length=25)

    class Meta():
        fields = ('amount', 'debit_account', 'debit_text', 'credit_account', 'credit_text')


class LoanSerializer(serializers.Serializer):
    name = serializers.CharField(label='Name for Loan', max_length=25)
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    
    class Meta():
        fields = ('name', 'amount')
