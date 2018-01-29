from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ObjectDoesNotExist


class LoginTests(TestCase):

    def setUp(self):
        self.client.logout()
        self.response = self.client.get('/account/signup/')

    def test_page_loads(self):
        self.assertEqual(self.response.status_code, 200)

    def test_page_loads_correct_template(self):
        self.assertTemplateUsed(self.response, 'account/signup.html')

    def test_new_user_is_created(self):
        # Ensure user doesn't exist
        try:
            newuser = User.objects.get(username='testuser1@test.com')
        except ObjectDoesNotExist:
            newuser = None

        # Assert that the user was found
        self.assertIsNone(newuser)

        # Create a post to the login page with the correct credentials
        self.client.post('/account/signup/', {'username': 'testuser1@test.com', 'password1': '123qweasd', 'password2': '123qweasd'})

        # Get the newly created user
        newuser = User.objects.get(username='testuser1@test.com')

        # Assert that the user was found
        self.assertIsNotNone(newuser)

    def test_email_and_username_are_equal(self):
        # Ensure user doesn't exist
        try:
            newuser = User.objects.get(username='testuser2@test.com')
        except ObjectDoesNotExist:
            newuser = None

        # Assert that the user was found
        self.assertIsNone(newuser)

        # Create a post to the login page with the correct credentials
        self.client.post('/account/signup/', {'username': 'testuser2@test.com', 'password1': '123qweasd', 'password2': '123qweasd'})

        # Get the newly created user
        newuser = User.objects.get(username='testuser2@test.com')

        # Assert that the user was found
        self.assertEqual(newuser.username, newuser.email)

    def test_duplicate_username_fails(self):
        # Create a post to the login page with the correct credentials
        self.client.post('/account/signup/', {'username': 'testuser3@test.com', 'password1': '123qweasd', 'password2': '123qweasd'})
        duplicate_response = self.client.post('/account/signup/', {'username': 'testuser3@test.com', 'password1': '123qweasd', 'password2': '123qweasd'})

        # Assert that the user was found
        self.assertContains(duplicate_response, 'There is already an account with that email address!')

    def test_invalid_email_username_fails(self):
        # Create a post to the login page with the correct credentials
        post_response = self.client.post('/account/signup/', {'username': 'testuser4', 'password1': '123qweasd', 'password2': '123qweasd'})

        # Assert that the user was found
        self.assertContains(post_response, "That does not appear to be a valid email address!")

    def test_new_user_is_inactive(self):

        # Create a post to the login page with the correct credentials
        self.client.post('/account/signup/', {'username': 'testuser4@test.com', 'password1': '123qweasd', 'password2': '123qweasd'})

        # Get the newly created user
        newuser = User.objects.get(username='testuser4@test.com')

        # Assert that the user was found
        self.assertFalse(newuser.is_active)
