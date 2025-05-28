from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.edit import DeleteView
from django.views import View

from .forms import AddCommentForm
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddCommentForm()
        return context
    
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
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    

class LeadCreateView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status')
    template_name = 'lead/leads_add.html'
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = Team.objects.filter(created_by=self.request.user)[0]
        return context
    
    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user).first()

        if team.leads.count() >= team.plan.max_leads:
            messages.error(self.request, "You have reached the lead limit for your plan.")
            return redirect('leads:list')

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()
        
        messages.success(self.request, 'The lead was created.')
        return redirect(self.get_success_url())


class ConvertLeadToClientView(View):
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=pk, created_by=request.user)
        team = Team.objects.filter(created_by=request.user).first()

        Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team=team
        )

        lead.converted_to_client = True
        lead.save()

        messages.success(request, 'The lead was converted to a client')
        return redirect('leads:list')
    

class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user).first()
            comment = form.save(commit=False)
            comment.team = team 
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)

            