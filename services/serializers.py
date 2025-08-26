from rest_framework import serializers
from .models import AirtimePurchase, DataPurchase

class AirtimePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirtimePurchase
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']

class DataPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPurchase
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at']
