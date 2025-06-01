from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views
from django.urls import path, include

from core.views import index, about
from user_profile.views import LogoutViaGet
from user_profile.forms import LoginForm

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/clients/', include('client.urls')),
    path('dashboard/teams/', include('team.urls')),
    path('dashboard/', include('user_profile.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('about/', about, name='about'),
    path('log-in/', views.LoginView.as_view(template_name='user_profile/login.html', authentication_form=LoginForm), name='login'),
    path('log-out/', LogoutViaGet.as_view(), name='logout'),
    # path('log-out/', LogoutViaGet.as_view(), name='logout'),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
