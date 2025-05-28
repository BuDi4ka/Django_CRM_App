from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from core.views import index, about
from user_profile.views import signup, LogoutViaGet, myaccount

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/myaccount/', myaccount, name='myaccount'),
    path('dashboard/', include('dashboard.urls')),
    path('about/', about, name='about'),
    path('sign-up/', signup, name='signup'),
    path('log-in/', views.LoginView.as_view(template_name='user_profile/login.html'), name='login'),
    path('log-out/', LogoutViaGet.as_view(), name='logout'),
    # path('log-out/', LogoutViaGet.as_view(), name='logout'),
    path("admin/", admin.site.urls),
]
