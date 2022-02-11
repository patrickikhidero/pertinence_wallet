from django.urls import path

from . import views

urlpatterns = [
    path('fund/', views.FundWalletView.as_view(), name='fund'),
    path('withdraw/', views.WithdrawWalletView.as_view(), name='withdraw'),
    path('pay/', views.PayWalletView.as_view(), name='pay'),
    path('', views.TransactionsView.as_view(), name='details')
]