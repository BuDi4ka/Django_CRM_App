from django.urls import path 

from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.LeadListView.as_view(), name='list'),
    path('add', views.LeadCreateView.as_view(), name='add'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/convert/', views.ConvertLeadToClientView.as_view(), name='convert'),
    path('<int:pk>/file/', views.FileCreateView.as_view(), name='file'),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment'),

]
