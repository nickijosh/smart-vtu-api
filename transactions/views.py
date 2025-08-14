from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Wallet
from .serializers import WalletSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WalletTransactionSerializer

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

