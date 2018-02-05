from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
from .models import Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            validate_email(username)
        except ValidationError:
            raise ValidationError("That does not appear to be a valid email address!")
        if User.objects.filter(models.Q(username=username) | models.Q(email=username)).exists():
            raise ValidationError("There is already an account with that email address!")
        return username

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'photo')
