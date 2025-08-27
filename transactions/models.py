from django.db import models
from users.models import User
from django.conf import settings
from decimal import Decimal
from users.models import Wallet

class Transaction(models.Model):
    TYPE_CHOICES = [('FUND', 'Fund'), ('AIRTIME', 'Airtime'), ('DATA', 'Data')]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    network = models.CharField(max_length=20, null=True, blank=True)
    data_plan = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    reference = models.CharField(max_length=60, unique=True, db_index=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} of {self.amount} by {self.user.username}"
    
        rid = self.reference or "-"
        return f"{self.user.username} - {self.transaction_type} - {self.amount} [{self.status}] ({rid})"

class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def credit(self, amount):
        self.balance += Decimal(amount)
        self.save()

    def debit(self, amount):
        if self.balance >= Decimal(amount):
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"