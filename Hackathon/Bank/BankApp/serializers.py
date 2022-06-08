from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Account, Customer, Ledger


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class LedgerSerializer (serializers.ModelSerializer):

    class Meta:
        model = Ledger
        fields = '__all__'


class AccountSerializer (serializers.ModelSerializer):
    movements = LedgerSerializer(many=True)

    class Meta:
        fields = ('pk', 'user', 'name', 'movements', 'balance')
        model = Account


class CustomerSerializer (serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        fields = ('user', 'pk', 'rank', 'personal_id', 'phone', 'accounts',  'can_make_loan', 'full_name')
        model = Customer

class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    debit_account = serializers.PrimaryKeyRelatedField(label='Debit Account', queryset=Account.objects.all())
    debit_text = serializers.CharField(label='Debit Account Text', max_length=25)
    credit_account = serializers.IntegerField(label='Credit Account Number')
    credit_text = serializers.CharField(label='Credit Account Text', max_length=25)

    class Meta:
        fields = ('amount', 'debit_account', 'debit_text', 'credit_account', 'credit_text')

class TransferExternalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    debit_account = serializers.IntegerField(label='Debit Account')
    debit_text = serializers.CharField(label='Debit Account Text', max_length=25)
    credit_account = serializers.IntegerField(label='Credit Account Number')
    credit_text = serializers.CharField(label='Credit Account Text', max_length=25)
    external_transfer = serializers.BooleanField()
    bank_code = serializers.CharField(label='bank_code')

    class Meta:
        fields = ('amount', 'debit_account', 'debit_text', 'credit_account', 'credit_text', 'external_transfer', 'bank_code')


class LoanSerializer(serializers.Serializer):
    name = serializers.CharField(label='Name for Loan', max_length=25)
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    
    class Meta:
        fields = ('name', 'amount')


class SearchSerializer(serializers.Serializer):
    search_term = serializers.CharField(label='Search', max_length=25)
    
    class Meta:
        fields = ('search_term')


class NewAccountSerializer(serializers.Serializer):
    new_account = serializers.CharField(label='New Account name', max_length=25)
    
    class Meta:
        fields = ('new_account')

RANK_CHOICES = (
    ("Basic", "Basic"),
    ("Silver", "Silver"),
    ("Gold", "Gold")
)

class NewUserCustomerSerializer(serializers.Serializer):
    username = serializers.CharField(label='username', max_length=25)
    first_name = serializers.CharField(label='First name', max_length=25)
    last_name = serializers.CharField(label='Last name', max_length=25)
    email = serializers.EmailField(label='email', max_length=25)
    rank = serializers.ChoiceField(label='rank', choices=RANK_CHOICES)
    personal_id = serializers.CharField(label='personal_id', max_length=25)
    phone = serializers.CharField(label='phone', max_length=25)
    
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'rank', 'personal_id', 'phone')

class ConvertSerializer(serializers.Serializer):
    currency1 = serializers.CharField(label='From Currency', max_length=3)
    amount = serializers.DecimalField(label='Amount', max_digits=9, decimal_places=2)
    currency2 = serializers.CharField(label='To Currency', max_length=3)
    
    class Meta:
        fields = ('currency1', 'amount', 'currency2')
