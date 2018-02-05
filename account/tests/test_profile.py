from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ProfileTests(TestCase):

    def setUp(self):
        # Create a valid User object for use in logging in
        self.user = User.objects.create_user(username='ProfileTestsUser', password='123')

    def test_page_redirects_with_anonymous_user(self):

        # Logout any current users
        self.client.logout()

        # Get the response from the profile page
        self.response = self.client.get('/account/profile', follow=True)

        # The page should redirect
        self.assertEqual(self.response.status_code, 200)

        # The page should redirect to home
        self.assertEqual(self.response.redirect_chain[0][0], '/account/login/?next=/account/profile')

    def test_page_loads_with_user_logged_in(self):

        # login
        self.client.login(username='ProfileTestsUser', password='123')

        # Load the profile page
        self.response = self.client.get('/account/profile')

        # The page should NOT redirect
        self.assertEqual(self.response.status_code, 200)

    def test_bio_updates_on_save(self):

        # login
        self.client.login(username='ProfileTestsUser', password='123')

        # Create a post to the login page with the correct credentials
        post_response = self.client.post('/account/profile', {'bio': 'bio updated!'})

        # Get the newly created user
        bio = User.objects.get(username='ProfileTestsUser').profile.bio

        # Assert that the user was found
        self.assertEqual(bio, 'bio updated!')

    # def test_page_loads_correct_template(self):
    #     self.assertTemplateUsed(self.response, 'account/profile.html')

    # def test_html_elements_exist(self):
    #     self.assertContains(self.response, '<form', 1)
    #     self.assertContains(self.response, 'method="post"', 1)
    #     self.assertContains(self.response, 'type="email"', 1)
    #     self.assertContains(self.response, 'type="password"', 2)
    #     self.assertContains(self.response, 'type="submit"', 1)
