from cProfile import label
from dataclasses import field
from locale import currency
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Customer, Account, Ledger, UID, Rank
from drf_braces.serializers.form_serializer import FormSerializer
from .forms import TransferForm
from django.contrib.auth.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('username', 'email', 'id', 'first_name', 'last_name')
        fields = '__all__'


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
    user = CurrentUserSerializer(read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        fields = ('pk', 'user', 'rank', 'personal_id', 'phone', 'accounts', 'can_make_loan')
        model = Customer
        #fields = '__all__'


class TransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    debit_account = serializers.PrimaryKeyRelatedField(label='Debit Account', queryset=Account.objects.none())
    debit_text = serializers.CharField(label='Debit Account Text', max_length=25)
    credit_account = serializers.IntegerField(label='Credit Account Number')
    credit_text = serializers.CharField(label='Credit Account Text', max_length=25)

    class Meta:
        fields = ('amount', 'debit_account', 'debit_text', 'credit_account', 'credit_text')

class RankSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rank
        fields = ('name', 'value')

class LoanSerializer(serializers.Serializer):
    name = serializers.CharField(label='Name for Loan', max_length=25)
    amount = serializers.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    
    class Meta:
        fields = ('name', 'amount')

class ExchangeSerializer(serializers.Serializer):
    from_currency = serializers.CharField(label='From Currency', max_length=3)
    amount = serializers.DecimalField(label='Amount', max_digits=9, decimal_places=2)
    to_currency = serializers.CharField(label='To Currency', max_length=3)


class SearchSerializer(serializers.Serializer):
    search_term = serializers.CharField(label='Search', max_length=25)
    
    class Meta:
        fields = ('search_term')


class NewAccountSerializer(serializers.Serializer):
    search_term = serializers.CharField(label='New Account name', max_length=25)
    
    class Meta:
        fields = ('new_account')


class NewUserCustomerSerializer(serializers.Serializer):
    username = serializers.CharField(label='username', max_length=25)
    first_name = serializers.CharField(label='First name', max_length=25)
    last_name = serializers.CharField(label='Last name', max_length=25)
    email = serializers.EmailField(label='email', max_length=25)
    #rank = RankSerializer(readyonly=True)
    rank = serializers.PrimaryKeyRelatedField( queryset=Rank.objects.all())
    #rank = serializers.CharField(label='rank', max_length=25)
    personal_id = serializers.CharField(label='personal_id', max_length=25)
    phone = serializers.CharField(label='phone', max_length=25)
    
    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'rank', 'personal_id', 'phone')

'''
class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            self._errors['username'] = self.error_class(['Username already exists.'])
        return self.cleaned_data


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', disabled=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
'''

