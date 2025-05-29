import csv

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Client
from .forms  import AddClientForm, AddCommentForm, AddFileForm

from team.models import Team

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/clients_list.html', {
        'clients': clients
    })


@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    comment_form = AddCommentForm()
    file_form = AddFileForm()

    if request.method == "POST":
        if 'submit_comment' in request.POST:
            comment_form = AddCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.team = team 
                comment.created_by = request.user
                comment.client = client
                comment.save()
                return redirect('clients:detail', pk=pk)

        elif 'submit_file' in request.POST:
            file_form = AddFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                file = file_form.save(commit=False)
                file.team = team
                file.client = client
                file.created_by = request.user
                file.save()
                return redirect('clients:detail', pk=pk)

    return render(request, 'client/clients_detail.html', {
        'client': client,
        'form': comment_form,
        'file_form': file_form,
    })


@login_required
def clients_add(request):
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == "POST":
        form = AddClientForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]

            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request, 'The client was created.')
 
            return redirect('clients:list')
    
    else:
        form = AddClientForm()

    return render(request, 'client/clients_add.html', {
        'form': form,
        'team': team,
        })


@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()

    messages.success(request, 'The client was deleted.')
    
    return redirect('clients:list')


@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes was saved')

            return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)

    return render(request, 'client/clients_edit.html', {
        'form': form,
        'client': client
    })


@login_required
def clients_export(request):
    clients = Client.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clients.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Client", "Description", "Created at", "Created by"])

    for client in clients:
        writer.writerow((client.name, client.description, client.created_at, client.created_by))
    
    return response