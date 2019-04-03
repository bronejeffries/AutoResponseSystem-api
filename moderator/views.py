from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Ars.decorators import Get_check
from Ars.models import Session
# Create your views here.


@Get_check
@login_required
def index(request):
    context = {}
    current_user_id=request.user.id
    user_sessions = Session.objects.filter(owner=current_user_id)
    context['sessions']=user_sessions
    inactive_session_count = user_sessions.filter(status="stopped").count()
    active_session_count = user_sessions.filter(status='running').count()
    context['active_count']=active_session_count
    context['inactive_count']=inactive_session_count
    # print(context)
    return render(request, 'moderator/index.html', context)
