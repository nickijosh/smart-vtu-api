from rest_framework import serializers
from .models import Wallet
from .models import Transaction
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'balance', 'created_at', 'updated_at']

class WalletTransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ("user", "wallet", "status", "created_at")