from django.test import TestCase, Client
from user.models import VirtualWalletUser


class ModelsTest(TestCase):
    def setUp(self):
        self.user = VirtualWalletUser.objects.create(
            password='cB987654321',
            email='test_create@pertinence.com',
            first_name='User',
            last_name='Test',
            birth_date='1956-097-03'
        )
        self.client = Client()

    def test_User_model_regular_user(self):
        self.user = VirtualWalletUser.objects.create(
            email='testmail@pertinence.com',
            password='cB987654321',
            first_name='User',
            last_name='Test',
            birth_date='1956-097-03'
        )

    def test_User_model_superuser(self):
        self.user = VirtualWalletUser.objects.create(
            email='myemail@pertinence.com',
            password='cB987654321',
            first_name='User',
            last_name='Test',
            birth_date='1956-097-03',
            is_superuser=True
        )

    def tearDown(self):
        self.user = VirtualWalletUser.objects.create(
            password='aA987654321',
            email='test_delete@example.com',
            first_name='User',
            last_name='Test',
            birth_date='1956-097-03'
        )
        self.user.delete()