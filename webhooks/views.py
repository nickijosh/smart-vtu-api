from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as drf_status
from transactions.models import Transaction, Wallet
from .models import WebhookLog

def _bad(msg):
    return Response({"detail": msg}, status=drf_status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def provider_webhook(request):
    # Simple shared-secret header check
    secret = request.headers.get("X-Webhook-Secret")
    if not secret or secret != getattr(settings, "WEBHOOK_SHARED_SECRET", ""):
        return Response({"detail": "Unauthorized webhook"}, status=drf_status.HTTP_401_UNAUTHORIZED)

    payload = request.data if isinstance(request.data, dict) else {}
    provider = payload.get("provider", "mock")
    reference = payload.get("reference")
    event = payload.get("event", "transaction.update")
    new_status = payload.get("status")  # 'success' | 'failed'

    # Log the webhook
    WebhookLog.objects.create(
        provider=provider,
        event=event,
        reference=reference,
        status=new_status,
        payload=payload
    )

    if not reference or new_status not in ("success", "failed"):
        return _bad("Missing reference or invalid status")

    try:
        tx = Transaction.objects.select_related("wallet", "user").get(reference=reference)
    except Transaction.DoesNotExist:
        return _bad("Transaction not found")

    if tx.status == new_status:
        return Response({"detail": "No change"}, status=drf_status.HTTP_200_OK)

    # If marking failed from pending/success, consider refund
    if new_status == "failed" and tx.status != "failed":
        # refund if it was previously debited
        if tx.transaction_type in ("airtime", "data"):
            tx.wallet.credit(tx.amount)

    tx.status = new_status
    tx.save(update_fields=["status"])

    return Response({"detail": "Transaction updated", "reference": reference, "status": new_status}, status=drf_status.HTTP_200_OK)
