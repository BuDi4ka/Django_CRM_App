from .models import Team

def team(request):
    return {'team': Team.objects.filter(created_by=request.user)[0]}