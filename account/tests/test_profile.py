from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ProfilePhotoUploadTests(TestCase):
    def _create_image(self):
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def setUp(self):
        # Create a valid User object for use in logging in
        self.user = User.objects.create_user(username='ProfilePhotoTestsUser', password='123')

        # login
        self.client.login(username='ProfilePhotoTestsUser', password='123')

        self.image = self._create_image()

    def tearDown(self):
        self.image.close()

    def test_profile_saved_with_photo(self):

        newuser = User.objects.get(username='ProfilePhotoTestsUser')

        post_response = self.client.post('/account/profile', {'bio': 'bio updated!', 'photo': self.image}, follow=True)

        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(bool(newuser.profile.photo.name))

    def test_profile_form_errors_with_invalid_image(self):
        not_an_image = SimpleUploadedFile('front.png', b'this is some text - not an image')

        newuser = User.objects.get(username='ProfilePhotoTestsUser')

        post_response = self.client.post('/account/profile', {'bio': 'bio updated!', 'photo': not_an_image}, follow=True)

        self.assertEqual(post_response.status_code, 200)
        self.assertFalse(bool(newuser.profile.photo.name))
        self.assertFormError(post_response, 'form', 'photo', 'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')


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
        self.client.post('/account/profile', {'bio': 'bio updated!'})

        # Get the newly created user
        bio = User.objects.get(username='ProfileTestsUser').profile.bio

        # Assert that the user was found
        self.assertEqual(bio, 'bio updated!')
