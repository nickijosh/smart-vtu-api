from django.db import models
from users.models import User
from django.conf import settings
from decimal import Decimal

class Transaction(models.Model):
    TYPE_CHOICES = [('FUND', 'Fund'), ('AIRTIME', 'Airtime'), ('DATA', 'Data')]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    service_provider = models.CharField(max_length=100, blank=True)
    phone_or_meter_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} of {self.amount} by {self.user.username}"

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