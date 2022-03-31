from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import INRTransaction, Book
from .serializers import TransactionSerializer, DebitCreditSerializer
from .services import DepositService


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def show_balance_view(request, *args, **kwargs):
#     try:
#         qs = User.objects.filter(username=request.user)[0].profile
#         serializer = WalletSerializer(qs)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_balance_view(request, *args, **kwargs):
    with transaction.atomic():
        # try:
        serializer_data = TransactionSerializer(data=request.data)
        serializer = DebitCreditSerializer(
            data={"debit": request.data.get('debit'), "credit": request.data.get('credit')})
        if serializer.is_valid(raise_exception=True):  # and serializer_data.is_valid(raise_exception=True):
            DepositService.execute({
                'username': request.user,
                'debitAcc': serializer_data.initial_data['debitAcc'],
                'creditAcc': serializer_data.initial_data['creditAcc'],
                'description': serializer_data.initial_data['description'],
                'debit': serializer.initial_data['debit'],
                'credit': serializer.initial_data['credit']
            })

        return Response({"Deposit successful."}, status=status.HTTP_200_OK)
    # except Exception as e:
    #     print(e)
    #     return Response({"Deposit unsuccessful."}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_balance_view(request, *args, **kwargs):
    try:
        login_user = str(request.user)
        if login_user != 'admin':
            qs = INRTransaction.objects.filter(user=request.user)
            data = []
            for i in qs:
                serializer = TransactionSerializer(i)
                data.append(serializer.data)
            return Response(data, status=200)
        else:
            queryset = INRTransaction.objects.all()
            data = []
            for i in queryset:
                serializer = TransactionSerializer(i)
                data.append(serializer.data)
            return Response(data, status=200)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)
