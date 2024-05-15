from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class FileServerUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class FileServerAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")