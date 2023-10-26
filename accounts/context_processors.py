from .models import LocalCouncil
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404



def local_council_id(request):
    if request.user.is_authenticated and request.user.is_local_council:
        local_council = get_object_or_404(LocalCouncil, user=request.user)
        local_council_id = local_council.id
    else:
        local_council_id = None
    
    return {'local_council_id': local_council_id}
