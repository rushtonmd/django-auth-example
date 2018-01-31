from django.test import TestCase
from django.contrib.auth.models import User


class PasswordChangeTests(TestCase):

    def setUp(self):
        # Create a valid User object for use in logging in
        self.user = User.objects.create_user(username='password change tests user', password='123')

    def test_reset_page_loads(self):
        self.client.login(username='password change tests user', password='123')
        self.response = self.client.get('/account/password-change/')
        self.assertEqual(self.response.status_code, 200)

    def test_reset_page_loads_correct_template(self):
        self.client.login(username='password change tests user', password='123')
        self.response = self.client.get('/account/password-change/')
        self.assertTemplateUsed(self.response, 'password_reset/password_change_form.html')

    def test_reset_page_redirects_with_no_session(self):
        self.client.logout()
        self.response = self.client.get('/account/password-change/', follow=True)

        self.assertEqual(self.response.status_code, 200)

        # The page should redirect to home
        self.assertEqual(self.response.redirect_chain[0][0], '/account/login/?next=/account/password-change/')
