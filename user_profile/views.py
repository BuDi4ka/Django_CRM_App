from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render


def signup(request):
    form = UserCreationForm()

    return render(request, 'user_profile/signup.html')