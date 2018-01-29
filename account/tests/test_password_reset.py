from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User


class PasswordResetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.response = self.client.get('/account/password/reset/')
