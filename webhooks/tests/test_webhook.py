from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from transactions.models import Wallet, Transaction

User = get_user_model()

class WebhookTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="wh", password="whpass")
        self.wallet = self.user.wallet
        self.wallet.balance = 1000
        self.wallet.save()

        # Create a pending airtime transaction (you should generate a reference in your real view)
        self.tx = Transaction.objects.create(
            user=self.user, wallet=self.wallet, transaction_type="airtime",
            amount="100.00", phone_number="08011122233", network="GLO",
            status="pending", reference="AIRTIME-TEST-REF-1"
        )

    def test_webhook_success(self):
        url = reverse("provider_webhook")
        payload = {
            "provider": "mock",
            "event": "transaction.update",
            "reference": "AIRTIME-TEST-REF-1",
            "status": "success"
        }
        res = self.client.post(url, payload, format="json", HTTP_X_WEBHOOK_SECRET="change_me_in_prod")
        self.assertEqual(res.status_code, 200)
        self.tx.refresh_from_db()
        self.assertEqual(self.tx.status, "success")

    def test_webhook_failed_refunds_wallet(self):
        # set to success first (simulate debit already happened)
        self.tx.status = "success"
        self.tx.save()
        bal_before = self.wallet.balance

        url = reverse("provider_webhook")
        payload = {
            "provider": "mock",
            "event": "transaction.update",
            "reference": "AIRTIME-TEST-REF-1",
            "status": "failed"
        }
        res = self.client.post(url, payload, format="json", HTTP_X_WEBHOOK_SECRET="change_me_in_prod")
        self.assertEqual(res.status_code, 200)

        self.tx.refresh_from_db()
        self.wallet.refresh_from_db()
        self.assertEqual(self.tx.status, "failed")
        self.assertEqual(self.wallet.balance, bal_before + self.tx.amount)  # refunded
