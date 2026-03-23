from django import forms
from django.forms import ModelForm
from .models import Genere, Author, Book
from django.contrib.auth.models import User


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        exclude = ["slug"]


class GenereForm(ModelForm):
    class Meta:
        model = Genere
        exclude = ["slug"]


class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ["slug"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ["last_name", "first_name", "username", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(render_value=False),
        }