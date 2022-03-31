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

        fields = ['user', 'debitAcc', 'creditAcc', 'description', 'debit', 'credit', 'dateTime']


class DebitCreditSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    debit = serializers.FloatField()
    credit = serializers.FloatField()

    def validate(self, data):
        debit = data.get('debit')
        credit = data.get('credit')
        if debit != credit:
            raise serializers.ValidationError('credit and debit should be equal')

        return debit, credit
