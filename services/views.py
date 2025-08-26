from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import AirtimePurchase, DataPurchase
from .serializers import AirtimePurchaseSerializer, DataPurchaseSerializer
from transactions.models import Transaction
from users.models import Wallet

# Airtime Purchase View
class AirtimePurchaseView(generics.CreateAPIView):
    serializer_class = AirtimePurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']

        # Deduct wallet balance
        wallet = Wallet.objects.get(user=user)
        if wallet.balance < amount:
            raise ValueError("Insufficient Balance")

        with transaction.atomic():
            wallet.balance -= amount
            wallet.save()

            purchase = serializer.save(user=user, status="SUCCESS")

            # Log transaction
            Transaction.objects.create(
                user=user,
                transaction_type="AIRTIME",
                amount=amount,
                status="SUCCESS",
                reference=f"AIRTIME-{purchase.id}"
            )
        return purchase

# Data Purchase View
class DataPurchaseView(generics.CreateAPIView):
    serializer_class = DataPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']

        # Deduct wallet balance
        wallet = Wallet.objects.get(user=user)
        if wallet.balance < amount:
            raise ValueError("Insufficient Balance")

        with transaction.atomic():
            wallet.balance -= amount
            wallet.save()

            purchase = serializer.save(user=user, status="SUCCESS")

            # Log transaction
            Transaction.objects.create(
                user=user,
                transaction_type="DATA",
                amount=amount,
                status="SUCCESS",
                reference=f"DATA-{purchase.id}"
            )
        return purchase
