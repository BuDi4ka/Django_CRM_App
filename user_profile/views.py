from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import UserProfile


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)

            return redirect("/log-in/")
    else:
        form = UserCreationForm()

    return render(request, 'user_profile/signup.html', {
        'form': form
        }
        )