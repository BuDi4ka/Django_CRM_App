from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full my-4 py-4 px-6 rounded-xl bg-grey-100'
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full my-4 py-4 px-6 rounded-xl bg-grey-100'
        }))


        