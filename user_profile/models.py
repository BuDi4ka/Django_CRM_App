from django.contrib.auth.models import User
from django.db import models

from team.models import Team

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    active_team_id = models.ForeignKey(Team, related_name='userprofiles', blank=True, null=True, on_delete=models.CASCADE)