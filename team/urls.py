from django.urls import path 

from . import views

app_name = 'team'

urlpatterns = [
    path('', views.teams_list, name='list'),
    path('<int:pk>/edit/', views.edit_team, name='edit'),
    path('<int:pk>/activate/', views.activate_team, name='activate'),
    path('<int:pk>/detail/', views.detail, name='detail'),
]
