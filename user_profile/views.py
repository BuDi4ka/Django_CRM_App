from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
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


class LogoutViaGet(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options'] 

    def get(self, request, *args, **kwargs):
        print("Custom GET logout called")
        return self.post(request, *args, **kwargs)
    
