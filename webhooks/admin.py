from django.contrib import admin
from .models import WebhookLog

@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ("id", "provider", "event", "reference", "status", "received_at")
    list_filter = ("provider", "status", "received_at")
    search_fields = ("reference", "event", "id")
