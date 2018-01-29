
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User


class LoginTests(TestCase):

    def setUp(self):
        # Create a valid User object for use in logging in
        self.user = User.objects.create_user(username='john', password='123')

        # self.client.login(username='john', password='123')
        self.response = self.client.get('/account/login/')

    def test_page_loads(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_loads_correct_template(self):
        self.assertTemplateUsed(self.response, 'account/login.html')

    def test_html_elements_exist(self):
        self.assertContains(self.response, '<form', 1)
        self.assertContains(self.response, 'method="post"', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_valid_post_creates_a_new_session(self):
        # logout the current user
        self.client.logout()

        # check that there is no current session
        self.assertNotIn('_auth_user_id', self.client.session)

        # Create a post to the login page with the correct credentials
        self.client.post('/account/login/', {'username': 'john', 'password': '123'})

        # There should now be a current valid session
        self.assertIn('_auth_user_id', self.client.session)

    def test_valid_post_redirects(self):
        # logout the current user
        self.client.logout()

        # check that there is no current session
        self.assertNotIn('_auth_user_id', self.client.session)

        # Create a post to the login page with the correct credentials
        post_response = self.client.post('/account/login/', {'username': 'john', 'password': '123'})

        # The page should redirect
        self.assertEqual(post_response.status_code, 302)

    def test_valid_post_redirects_to_home(self):
        # logout the current user
        self.client.logout()

        # check that there is no current session
        self.assertNotIn('_auth_user_id', self.client.session)

        # Create a post to the login page with the correct credentials
        post_response = self.client.post('/account/login/', {'username': 'john', 'password': '123'}, follow=True)

        # The page should redirect
        self.assertEqual(post_response.status_code, 200)

        # The page should redirect to home
        self.assertEqual(post_response.redirect_chain[0][0], '/')

    # An invalid post request should:
    # - not create a new session
    # - respond with a 200 status_code
    # - contain an error message
    def test_invalid_post(self):
        # logout the current user
        self.client.logout()

        # check that there is no current session
        self.assertNotIn('_auth_user_id', self.client.session)

        # Create a post to the login page with the correct credentials
        post_response = self.client.post('/account/login/', {'username': 'john', 'password': '555'})

        # There should NOT be a current valid session
        self.assertNotIn('_auth_user_id', self.client.session)

        # The page should not redirect
        self.assertEqual(post_response.status_code, 200)

        # The page should contain errors
        self.assertContains(post_response, 'class="alert alert-danger"', 1)
