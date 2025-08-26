from django.db import models
from django.conf import settings
from transactions.models import Transaction

class AirtimePurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    network = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="PENDING")  # PENDING, SUCCESS, FAILED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Airtime {self.amount} for {self.phone_number}"

class DataPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)  # e.g MTN 1GB
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    network = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data {self.plan} for {self.phone_number}"
