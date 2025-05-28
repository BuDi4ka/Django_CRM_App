from django.urls import path 

from . import views

urlpatterns = [
    path('', views.clients_list, name='clients-list'),
    path('<int:pk>/', views.clients_detail, name='clients-detail'),
    path('add/', views.clients_add, name='clients-add')
]
