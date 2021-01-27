from django.core.management import call_command
from django.test import TestCase, Client

from authapp.models import ShopUser


class TestAuthUserTestCase(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        self.client = Client()

        self.superuser = ShopUser.objects.create_superuser('django', 'django@gb.local', 'geekbrains')
        self.user = ShopUser.objects.create_user('test1', 'test1@gb.local', 'geekbrains')
        self.user_with_fn = ShopUser.objects.create_user('test2', 'test2@gb.local', 'geekbrains', first_name='Test2')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
