from django.urls import path
from .views import WalletDetailView
from .views import AddFundsView, WithdrawFundsView
from .views import BuyAirtimeView, BuyDataView, TransactionHistoryView

urlpatterns = [
    path('wallet/', WalletDetailView.as_view(), name='wallet-detail'),
    path("wallet/add/", AddFundsView.as_view(), name="add-funds"),
    path("wallet/withdraw/", WithdrawFundsView.as_view(), name="withdraw-funds"),
    path("buy-airtime/", BuyAirtimeView.as_view(), name="buy_airtime"),
    path("buy-data/", BuyDataView.as_view(), name="buy_data"),
    path("history/", TransactionHistoryView.as_view(), name="transaction_history"),
]
