from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models


class CustomLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class CustomUserCreationForm(UserCreationForm):
    # email = EmailField(label=_("Email address"), required=True, help_text=_("Required."))

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
