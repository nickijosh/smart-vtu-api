from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from transactions.models import Wallet

User = get_user_model()

class WalletEndpointsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="a1b2c3d4")
        login = self.client.post(reverse("login"), {"username":"alice", "password":"a1b2c3d4"}, format="json")
        self.token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_add_funds(self):
        res = self.client.post("/api/transactions/wallet/add-funds/", {"amount": "1000.00"}, format="json")
        self.assertEqual(res.status_code, 200)
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(str(wallet.balance), "1000.00")

    def test_withdraw(self):
        self.client.post("/api/transactions/wallet/add-funds/", {"amount": "500.00"}, format="json")
        res = self.client.post("/api/transactions/wallet/withdraw/", {"amount": "200.00"}, format="json")
        self.assertEqual(res.status_code, 200)
        wallet = Wallet.objects.get(user=self.user)
        self.assertEqual(str(wallet.balance), "300.00")
