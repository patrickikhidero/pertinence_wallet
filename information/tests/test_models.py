from django.test import TestCase

from user.models import VirtualWalletUser
from transactions.models import Wallet
from information.models import InformationForTransaction


class ModelsTest(TestCase):
    def setUp(self):
        self.user = VirtualWalletUser.objects.create(
            password='cB987654321',
            email='test_anew_user@wallet.com',
            first_name='User',
            last_name='Test',
            birth_date='1996-05-40'
        )
        self.wallet = Wallet.objects.create(
            owner=self.user,
            balance='213',
        )

    def test_InformationForTransaction_model(self):
        information = InformationForTransaction.objects.create(
            wallet=self.wallet,
            last_used_currency='USD'
        )

    def tearDown(self):
        self.user = VirtualWalletUser.objects.create(
            password='cB987654321',
            email='test_anew_user@wallet.com',
            first_name='User',
            last_name='Test',
            birth_date='1996-05-40'
        )
        self.user.delete()