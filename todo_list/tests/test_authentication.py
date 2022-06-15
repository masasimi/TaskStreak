from django.test import TestCase, Client
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    def test_not_authenticated(self):
        """未ログイン時にレスポンスを返さないことをチェック"""
        client = Client()
        client.logout()
        response = client.get('/')
        self.assertEqual(response.context, None)

    def test_authenticated(self):
        """ユーザがログインに成功することをチェック"""
        client = Client()
        client.force_login(User.objects.create_user('tester'))
        response = client.get('/')
        self.assertTrue('username' in response.context)
        self.assertEqual(response.context['username'], 'tester')