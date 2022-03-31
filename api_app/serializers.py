from rest_framework import serializers

from .models import Profile, INRTransaction, Book


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # balance should be integer and positive
        balance = serializers.FloatField()

        @staticmethod
        def validate(data):
            balance = data.get('balance')
            if balance < 0.0:
                raise serializers.ValidationError('amount cannot be negative')

        fields = ['balance', ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = INRTransaction
        dr = serializers.FloatField()
        cr = serializers.FloatField()

        @staticmethod
        def validate(data):
            dr = data.get('dr')
            cr = data.get('cr')
            if dr != cr:
                raise serializers.ValidationError('credit and debit should be equal')

        fields = ['user', 'debitAcc', 'creditAcc', 'description', 'dr', 'cr', 'dateTime']
