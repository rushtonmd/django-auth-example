from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User


class LoginTests(TestCase):

    def setUp(self):
        # Create a valid User object for use in logging in
        self.user = User.objects.create_user(username='john', password='123')

        # self.client.login(username='john', password='123')
        self.response = self.client.get('/account/signup/')

    def test_page_loads(self):
        self.assertEqual(self.response.status_code, 200)
