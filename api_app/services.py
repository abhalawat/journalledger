from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from service_objects.services import Service

from .models import Book, INRTransaction, BookEntries


class DepositService(Service):
    username = serializers.CharField(max_length=30)
    debitAcc = serializers.CharField(max_length=30)
    creditAcc = serializers.CharField(max_length=30)
    description = serializers.CharField(max_length=50)
    debit = serializers.FloatField()
    credit = serializers.FloatField()

    def process(self):
        user = self.data['username']
        debit_acc = self.data['debitAcc']
        credit_acc = self.data['creditAcc']
        description = self.data['description']
        debit = self.data['debit']
        credit = self.data['credit']

        qs_debit = Book.objects.filter(book_name=debit_acc)  # .exists()
        qs_credit = Book.objects.filter(book_name=credit_acc)  # .exists()
        if not qs_debit.exists():
            qs_debit = Book.objects.create(book_name=debit_acc)
        else:
            qs_debit = qs_debit.first()

        if not qs_credit.exists():
            qs_credit = Book.objects.create(book_name=credit_acc)
        else:
            qs_credit = qs_credit.first()

        debit_book_details = BookEntries(book_name=debit_acc,
                                         description=description,
                                         debit=debit)
        debit_book_details.save()

        credit_book_details = BookEntries(book_name=credit_acc,
                                          description=description,
                                          credit=credit)
        credit_book_details.save()

        transaction1 = INRTransaction(user=user, debitAcc=qs_debit, creditAcc=qs_credit,
                                      description=description, debit=debit, credit=credit, dateTime=timezone.now())
        transaction1.save()


class WithdrawService(Service):
    username = serializers.CharField(max_length=30)
    withdraw = serializers.FloatField()

    def process(self):
        amount = self.data['withdraw']
        user = self.data['username']

        qs = User.objects.select_for_update().filter(username=user)[0].profile
        if qs.balance >= amount:
            qs.balance = qs.balance - amount
            qs.save()
            transaction1 = INRTransaction(user=user, withdraw=amount, balance=qs.balance,
                                          dateTime=timezone.now())
            transaction1.save()
        else:
            raise serializers.ValidationError("amount is greater than balance")
