from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# The Profile class will act as an extension of the User class.
# This is done so that the base functionality of the User
# class including auth will not be modified.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


# When a new User is created, also create the cooresponding
# Profile object and link them together
# Reference: https://docs.djangoproject.com/en/2.0/topics/signals/
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    # If the new user is created, also create a new Profile
    if created:
        Profile.objects.create(user=instance)

    # Save the profile of the user (instance)
    instance.profile.save()
