from django.urls import path 

from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.clients_list, name='list'),
    path('<int:pk>/', views.clients_detail, name='detail'),
    path('<int:pk>/delete/', views.clients_delete, name='delete'),
    path('<int:pk>/edit/', views.clients_edit, name='edit'),
    path('<int:pk>/comment/', views.clients_detail, name='comment'),
    path('<int:pk>/file/', views.clients_detail, name='file'),
    path('add/', views.clients_add, name='add'),
    path('export/', views.clients_export, name='export')
]
