from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Wallet
from .serializers import WalletSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WalletTransactionSerializer
from .models import Transaction
from .serializers import TransactionSerializer


class WalletDetailView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet

class AddFundsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WalletTransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            wallet.credit(amount)
            return Response({"message": "Funds added successfully", "balance": wallet.balance}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawFundsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = WalletTransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            wallet, created = Wallet.objects.get_or_create(user=request.user)
            if wallet.debit(amount):
                return Response({"message": "Withdrawal successful", "balance": wallet.balance}, status=status.HTTP_200_OK)
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuyAirtimeView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        phone_number = request.data.get("phone_number")
        network = request.data.get("network")

        wallet = Wallet.objects.get(user=request.user)

        if wallet.balance < float(amount):
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct wallet balance
        wallet.balance -= float(amount)
        wallet.save()

        # Log transaction
        transaction = Transaction.objects.create(
            user=request.user,
            wallet=wallet,
            transaction_type="airtime",
            amount=amount,
            phone_number=phone_number,
            network=network,
            status="success"
        )

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class BuyDataView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        phone_number = request.data.get("phone_number")
        network = request.data.get("network")
        data_plan = request.data.get("data_plan")

        wallet = Wallet.objects.get(user=request.user)

        if wallet.balance < float(amount):
            return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct wallet balance
        wallet.balance -= float(amount)
        wallet.save()

        # Log transaction
        transaction = Transaction.objects.create(
            user=request.user,
            wallet=wallet,
            transaction_type="data",
            amount=amount,
            phone_number=phone_number,
            network=network,
            data_plan=data_plan,
            status="success"
        )

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-created_at")
