from .models import Transaction, Account


def CreateTransaction(description, from_acc, to_acc, amount, customer_id):
    try:
        transaction =Transaction()
        # id = uuid.uuid4()  # import
        transaction(
            description=description,
            amount=amount,
            t_type="CREDIT",
            account_id=to_acc,
            customer_id=customer_id
        )
        transaction.save()
        transaction(
            description=description,
            amount=amount,
            t_type="DEBIT",
            account_id=from_acc,
            customer_id=customer_id
        )
        transaction.save()
    except:
        print("failed to create Transaction")


def CompleteTransaction(from_acc, to_acc, amount, fromnew, tonew, customer_id):
    account = Account()
    #from_account = Account.objects.get(id=from_acc, customer_id=customer_id)
    Account.objects.filter(id=from_acc).update(amount=fromnew)
    account.save()
    # to_account = Account.objects.get(id=to_acc)
    Account.objects.filter(id=to_acc).update(amount=tonew)
    account.save()
