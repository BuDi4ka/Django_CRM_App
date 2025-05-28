from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import DeleteView


from .forms import AddLeadForm
from .models import Lead

from client.models import Client
from team.models import Team


class LeadListView(ListView):
    model = Lead
    template_name = 'lead/leads_list.html'
    context_object_name = 'leads'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, converted_to_client=False)

        return queryset

    
class LeadDetailView(DetailView):
    model = Lead
    context_object_name = 'lead'
    template_name = 'lead/leads_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


class LeadDeleteView(DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def get_template_names(self):
        return []   

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


class LeadUpdateView(UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status')
    template_name = 'lead/leads_edit.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get_success_url(self):
        return reverse_lazy('leads:list')


class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status')
    template_name = 'lead/leads_add.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('leads:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.filter(created_by=self.request.user)[0]
        return context



@login_required
def leads_add(request):
    team = Team.objects.filter(created_by=request.user)[0]
    
    if request.method == "POST":
        form = AddLeadForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]

            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()

            messages.success(request, 'The lead was created.')
 
            return redirect('leads:list')
    
    else:
        form = AddLeadForm()

    return render(request, 'lead/leads_add.html', {
        'form': form,
        'team': team,
        })


@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user)
    team = Team.objects.filter(created_by=request.user)[0]

    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description = lead.description,
        created_by = request.user,
        team = team
        )
    
    lead.converted_to_client = True
    lead.save()

    messages.success(request, 'The lead was converted to a client')

    return redirect('leads:list')