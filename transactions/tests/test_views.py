from datetime import date, timedelta
from collections import OrderedDict

from django.test import TestCase, Client
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework import status

from user.models import VirtualWalletUser
from transactions.models import Wallet, Transaction
from transactions.views import  WithdrawWalletView, PayWalletView, TransactionsView


class ViewsTesting(TestCase):
    def setUp(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_create@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )

        self.wallet = Wallet.objects.create(
            owner=self.user,
            balance='100',
        )

        self.client = Client()

    def test_fill_without_auth(self):
        _call_fill_view_test_template(self=self,
                                      value='100',
                                      endpoint="/api/v1/transactions/fill/",
                                      user=self.user,
                                      is_authenticated=False,
                                      response_code=status.HTTP_403_FORBIDDEN
                                      )

    def test_fill_zero(self):
        _call_fill_view_test_template(self=self,
                                      value='0',
                                      endpoint="/api/v1/transactions/fill/",
                                      user=self.user,
                                      is_authenticated=True,
                                      response_code=status.HTTP_400_BAD_REQUEST
                                      )

    def test_fill(self):
        _call_fill_view_test_template(self=self,
                                      value='100',
                                      endpoint="/api/v1/transactions/fill/",
                                      user=self.user,
                                      is_authenticated=True,
                                      response_code=status.HTTP_200_OK
                                      )

    def test_withdraw_without_auth(self):
        _call_withdraw_view_test_template(self=self,
                                          value='100',
                                          endpoint="/api/v1/transactions/withdraw/",
                                          user=self.user,
                                          is_authenticated=False,
                                          response_code=status.HTTP_403_FORBIDDEN)

    def test_withdraw_zero(self):
        _call_withdraw_view_test_template(self=self,
                                          value='0',
                                          endpoint="/api/v1/transactions/withdraw/",
                                          user=self.user,
                                          is_authenticated=True,
                                          response_code=status.HTTP_400_BAD_REQUEST)

    def test_withdraw_too_many(self):
        _call_withdraw_view_test_template(self=self,
                                          value=1e30,
                                          endpoint="/api/v1/transactions/withdraw/",
                                          user=self.user,
                                          is_authenticated=True,
                                          response_code=status.HTTP_400_BAD_REQUEST)

    def test_withdraw(self):
        _call_withdraw_view_test_template(self=self,
                                          value='1',
                                          endpoint="/api/v1/transactions/withdraw/",
                                          user=self.user,
                                          is_authenticated=True,
                                          response_code=status.HTTP_200_OK)

    def test_pay_view(self):
        factory = APIRequestFactory()
        view = PayWalletView.as_view()

        receiver = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='receiver@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )

        receiver_wallet = Wallet.objects.create(
            owner=receiver,
            balance='100',
        )

        data = {
            'value': '1',
            'email': 'receiver@example.com'
        }

        request = factory.post('/api/v1/transactions/pay/', data)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_view_authenticated(self):
        _setup_transaction_view_test_template(self=self,
                                              transaction_start_date=date.today(),
                                              transaction_end_date=date.today(),
                                              is_authenticated=True,
                                              response_code=status.HTTP_200_OK)

    def test_transaction_view_not_authenticated(self):
        _setup_transaction_view_test_template(self=self,
                                              transaction_start_date=date.today(),
                                              transaction_end_date=date.today(),
                                              is_authenticated=False,
                                              response_code=status.HTTP_403_FORBIDDEN)

    def test_transaction_view_response_data(self):
        transaction_custom_date = str(date.today()-timedelta(days=1))
        value = '111.00'
        response_data = [OrderedDict(
            [('date', transaction_custom_date),
             ('type', 'payment_withdraw'),
             ('value', value)]
        )]
        _setup_transaction_view_test_template(
            self=self,
            transaction_start_date=transaction_custom_date,
            transaction_end_date=transaction_custom_date,
            is_authenticated=True,
            response_code=status.HTTP_200_OK,
            response_data=response_data,
            value=value
        )

    def tearDown(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_delete@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1987-08-30'
        )
        self.user.delete()


def _setup_fill_and_withdraw_template(self, view, value, user, endpoint, is_authenticated, response_code):
    """
    Performs regular actions which are required for request creation, user authentication and response validation
    during wallet fill and withdraw
    """
    factory = APIRequestFactory()

    data = {
        'value': value
    }

    request = factory.post(endpoint, data)
    if is_authenticated:
        force_authenticate(request, user=user)
    response = view(request)
    self.assertEqual(response.status_code, response_code)


def _call_fill_view_test_template(self, value, user, endpoint, is_authenticated, response_code):
    view = FillWalletView.as_view()
    _setup_fill_and_withdraw_template(self, view, value, user, endpoint, is_authenticated, response_code)


def _call_withdraw_view_test_template(self, value, user, endpoint, is_authenticated, response_code):
    view = WithdrawWalletView.as_view()
    _setup_fill_and_withdraw_template(self, view, value, user, endpoint, is_authenticated, response_code)


def _setup_transaction_view_test_template(
        self, transaction_start_date, transaction_end_date, is_authenticated, response_code, value=None, response_data=None
):
    """
        Creates test data and performs regular actions which are required for request creation, user authentication and
        response validation during wallet transactions
    """
    factory = APIRequestFactory()
    view = TransactionsView.as_view()

    transaction = Transaction.objects.create(
        wallet=self.wallet,
        email='test_create@example.com',
        type='payment_received',
        value=100
    )

    transaction = Transaction.objects.create(
        wallet=self.wallet,
        email='test_create@example.com',
        type='payment_fill',
        value=50
    )

    if value:
        transaction = Transaction.objects.create(
            wallet=self.wallet,
            email='test_create@example.com',
            type='payment_withdraw',
            value=value
        )

        transaction_yesterday = Transaction.objects.get(value=value)
        transaction_yesterday.date = str(transaction_start_date)
        transaction_yesterday.save(update_fields=['date'])

    endpoint = f"http://0.0.0.0:8000/api/v1/transactions/?" \
               f"start_date={str(transaction_start_date)}&" \
               f"end_date={str(transaction_end_date)}"
    request = factory.get(endpoint)
    if is_authenticated:
        force_authenticate(request, user=self.user)
    response = view(request)
    self.assertEqual(response.status_code, response_code)
    if response_data:
        self.assertEqual(response.data, response_data)