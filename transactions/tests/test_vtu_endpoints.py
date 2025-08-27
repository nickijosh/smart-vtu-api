from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from transactions.models import Wallet, Transaction

User = get_user_model()

class VTUEndpointsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="p455word!")
        login = self.client.post(reverse("login"), {"username":"bob", "password":"p455word!"}, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        Wallet.objects.filter(user=self.user).update(balance=1000)

    def test_buy_airtime(self):
        res = self.client.post("/api/transactions/buy-airtime/", {
            "amount": "200.00", "phone_number": "08012345678", "network": "MTN"
        }, format="json")
        self.assertEqual(res.status_code, 201)
        tx = Transaction.objects.filter(user=self.user, transaction_type="airtime").first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.status, "success")

    def test_buy_data(self):
        res = self.client.post("/api/transactions/buy-data/", {
            "amount": "300.00", "phone_number": "08098765432", "network": "Airtel", "data_plan": "1GB"
        }, format="json")
        self.assertEqual(res.status_code, 201)
        tx = Transaction.objects.filter(user=self.user, transaction_type="data").first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.status, "success")
