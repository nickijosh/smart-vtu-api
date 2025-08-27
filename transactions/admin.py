from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "transaction_type", "network",
        "phone_number", "data_plan", "amount", "status", "created_at"
    )
    list_filter = ("transaction_type", "status", "network", "created_at")
    search_fields = ("user__username", "user__email", "phone_number", "id")
    readonly_fields = ("created_at",)
