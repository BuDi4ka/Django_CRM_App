from django.urls import path 

from . import views

urlpatterns = [
    path('', views.leads_list, name='leads-list'),
    path('<int:pk>/', views.leads_detail, name='leads-detail'),
    path('add-lead', views.add_lead, name='add-lead'),
]
