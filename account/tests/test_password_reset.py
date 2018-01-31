from django.test import TestCase


class PasswordResetTests(TestCase):

    def test_reset_page_loads(self):
        self.response = self.client.get('/account/password-reset/')
        self.assertEqual(self.response.status_code, 200)

    def test_reset_page_loads_correct_template(self):
        self.response = self.client.get('/account/password-reset/')
        self.assertTemplateUsed(self.response, 'password_reset/password_reset_form.html')

    def test_reset_done_page_loads(self):
        self.response = self.client.get('/account/password-reset/done')
        self.assertEqual(self.response.status_code, 200)

    def test_reset_done_page_loads_correct_template(self):
        self.response = self.client.get('/account/password-reset/done')
        self.assertTemplateUsed(self.response, 'account/generic_message.html')

    def test_reset_complete_page_loads(self):
        self.response = self.client.get('/account/reset/done')
        self.assertEqual(self.response.status_code, 200)

    def test_reset_complete_page_loads_correct_template(self):
        self.response = self.client.get('/account/reset/done')
        self.assertTemplateUsed(self.response, 'account/generic_message.html')

    def test_reset_token_page_loads(self):
        self.response = self.client.get('/account/reset/<uidb64>/<token>/')
        self.assertEqual(self.response.status_code, 200)

    def test_reset_token_page_loads_correct_template(self):
        self.response = self.client.get('/account/reset/<uidb64>/<token>/')
        self.assertTemplateUsed(self.response, 'password_reset/password_reset_confirm.html')
