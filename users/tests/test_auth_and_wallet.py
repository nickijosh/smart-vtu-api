from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from transactions.models import Wallet

User = get_user_model()

class AuthAndWalletTests(APITestCase):
    def test_signup_creates_wallet(self):
        url = reverse("signup")
        data = {"username": "w4user", "password": "pass12345", "email": "w4@example.com"}
        res = self.client.post(url, data, format="json")
        self.assertIn(res.status_code, [200, 201])
        user = User.objects.get(username="w4user")
        self.assertTrue(Wallet.objects.filter(user=user).exists())

    def test_login_jwt(self):
        User.objects.create_user(username="tokuser", password="secretpass")
        url = reverse("login")
        res = self.client.post(url, {"username":"tokuser", "password":"secretpass"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
