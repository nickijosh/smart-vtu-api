from django.db import models
from django.utils import timezone

class WebhookLog(models.Model):
    provider = models.CharField(max_length=50, default="mock")
    event = models.CharField(max_length=100, blank=True, null=True)
    reference = models.CharField(max_length=80, db_index=True, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    payload = models.JSONField()
    received_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.provider} {self.event} {self.reference} [{self.status}]"
