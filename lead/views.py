from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def add_lead(request):
    return render(request, 'lead/add_lead.html')