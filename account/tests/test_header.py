from django.test import TestCase
from django.contrib.auth.models import User


class HeaderTests(TestCase):

    def setUp(self):
        # Create a valid User object for use in logging in
        self.user = User.objects.create_user(username='HeaderTestsUser', password='123')

    def test_page_loads(self):
        # Use the login page to test the header
        self.response = self.client.get('/account/login/')

        # The page should load with a 200 response
        self.assertEqual(self.response.status_code, 200)

    def test_header_loads(self):

        # Use the login page to test the header
        self.response = self.client.get('/account/login/')

        # The admin-header should be in the response
        self.assertContains(self.response, 'account-header', 1)

    def test_signin_link_appears_when_no_user_is_logged_in(self):
        # logout the current user
        self.client.logout()

        # Use the login page to test the header
        self.response = self.client.get('/account/login/')

        # The admin-header should be in the response
        self.assertContains(self.response, 'account-signin-link', 1)

    def test_signout_link_appears_when_user_logged_in(self):
        # logout the current user
        self.client.login(username='HeaderTestsUser', password='123')

        # Use the login page to test the header
        self.response = self.client.get('/account/login/')

        # The admin-header should be in the response
        self.assertContains(self.response, 'account-signout-link', 1)
