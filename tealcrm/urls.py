from django.contrib import admin
from django.urls import path, include

from core.views import index, about
from user_profile.views import signup

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('sign-up/', signup, name='signup'),
    path("admin/", admin.site.urls),
]
