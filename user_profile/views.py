from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UserProfile
from .forms import SignupForm

from team.models import Team


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(user=user)
            
            team = Team.objects.create(name=f"The team of {request.name}", created_by=request.user)
            team.members.add(request.user)
            team.save()

            return redirect("/log-in/")
    else:
        form = SignupForm()

    return render(request, 'user_profile/signup.html', {
        'form': form
        }
        )


class LogoutViaGet(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options'] 

    def get(self, request, *args, **kwargs):
        print("Custom GET logout called")
        return self.post(request, *args, **kwargs)
    

@login_required
def myaccount(request):
    team = Team.objects.filter(created_by=request.user)[0]

    return render(request, 'user_profile/myaccount.html', {
        'team': team
    })