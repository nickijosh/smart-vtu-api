from django.urls import path
from .views import WalletDetailView
from .views import AddFundsView, WithdrawFundsView

urlpatterns = [
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path("wallet/add/", AddFundsView.as_view(), name="add-funds"),
    path("wallet/withdraw/", WithdrawFundsView.as_view(), name="withdraw-funds"),
]
