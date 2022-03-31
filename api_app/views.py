from django.db import transaction
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import INRTransaction, BookEntries, Book
from .serializers import TransactionSerializer


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
        try:
# {"debitAcc": "bank",
#  "creditAcc": "wallet",
#  "description": "hello",
#  "dr": "43",
#  "cr": "43"}
            try:
                Book.objects.get(book_name=request.data.get('debitAcc'))
            except:
                Book.objects.create(book_name=request.data.get('debitAcc'))

            try:
                Book.objects.get(book_name=request.data.get('creditAcc'))
            except:
                Book.objects.create(book_name=request.data.get('creditAcc'))

            serializer = TransactionSerializer(data=request.data)
            # print(serializer.initial_data['debitAcc'])
            # if serializer.is_valid(raise_exception=True):

            debit_book_details = BookEntries(book_name=serializer.initial_data['debitAcc'],
                                             description=serializer.initial_data['description'],
                                             debit=serializer.initial_data['dr'])
            debit_book_details.save()

            credit_book_details = BookEntries(book_name=serializer.initial_data['creditAcc'],
                                              description=serializer.initial_data['description'],
                                              credit=serializer.initial_data['cr'])
            credit_book_details.save()

            # print(Book.objects.create(book_name="A"))
            # print(Book.objects.get(book_name="A"))

            return Response({"Deposit successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"Deposit unsuccessful."}, status=400)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def withdraw_balance_view(request, *args, **kwargs):
#     try:
#         with transaction.atomic():
#             serializer = WithdrawSerializer(data=request.data)
#             # {"amount": 2}
#             if serializer.is_valid(raise_exception=True):
#                 WithdrawService.execute({
#                     'username': request.user,
#                     'withdraw': serializer.initial_data['amount']
#                 })
#             return Response({"Withdraw successful."}, status=status.HTTP_200_OK)
#     except Exception as e:
#         print(e)
#         return Response({"Something went wrong. Please try again later."}, status=status.HTTP_404_NOT_FOUND)


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
