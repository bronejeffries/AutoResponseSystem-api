from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Ars.decorators import Get_check,Post_check
from Ars.models import Session
import random
from django.utils import timezone
from Ars.Serializers import SessionSerializer


def get_session_by_key(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
    except Session.MultipleObjectsReturned:
        session = Session.objects.filter(session_key=session_key
                                         ).last()
        return session
    except Session.DoesNotExist:
        return False
    else:
        return session


@login_required
@Post_check
def sessionCreate(request):
    owner = request.user.id
    # generate session_key from session_name
    session_key = request.POST['session_name'] +"-" + str(generateRandom())+"-" + str(generateRandom())
    new_session_data = {
    'owner':owner,
    'session_key':session_key
    }
    new_session = SessionSerializer(data=new_session_data)
    if new_session.is_valid():
        new_session.save()
        return HttpResponseRedirect(reverse('moderator:categorycreate',args=(new_session.data['id'],)))

@login_required
@Get_check
def sessionDetails(request,session_pk):
    details = {}
    session = get_session_by_id(session_pk)
    if session and (session.owner.id==request.user.id):
        details['polls']=session.question_set.all()
        details['topics']=session.topic_set.all()
        details['submissions']=session.submission_set.all()
        details['session_key']=session.session_key

    return render(request,'moderator/sessiondetails.html',details)


def get_session_by_id(pk):
    session={}
    try:
        session = Session.objects.get(id=pk)
    except Session.DoesNotExist:
        return false
    else:
        return session

def generateRandom():
    return random.randint(1, 10000001)

@login_required
@Get_check
def categoryIndex(request,pk):
    context=dict()
    polls_count=topic_count=0
    context['session_pk']=pk
    user = request.user.id
    user_sessions=Session.objects.filter(owner=user)
    for session in user_sessions:
        polls_count += session.question_set.count()
        topic_count += session.topic_set.count()

    context['polls_count']=polls_count
    context['topic_count']=topic_count

    return render(request,'moderator/categories.html',context)
