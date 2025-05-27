from django.urls import path 

from . import views

urlpatterns = [
    path('', views.leads_list, name='leads-list'),
    path('<int:pk>/', views.leads_detail, name='leads-detail'),
    path('<int:pk>/delete', views.leads_delete, name='leads-delete'),
    path('<int:pk>/edit', views.leads_edit, name='leads-edit'),
    path('<int:pk>/convert/', views.convert_to_client, name='leads-convert'),
    path('add-lead', views.add_lead, name='add-lead'),
]
