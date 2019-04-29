from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Ars.decorators import Get_check,Post_check
from Ars.models import Session, Topic, Question
from Ars.Serializers import SessionSerializer, TopicSerializer, QuestionSerializer, OptionSerializer
from Ars.views import Makeqrfrom
from .presentationViews import (makeQuestionPresentation as mqp,
                                makeTopicpresentation as mtp )

@login_required
@Post_check
def deleteTopic(request,session_pk,pk):
    topic = get_topic(pk)
    if topic:
        topic.delete()
        return HttpResponseRedirect(reverse('moderator:sessionDetails',args=(session_pk,)))


@login_required
@Post_check
def deleteQuestion(request,session_pk,pk):
    question = get_Question(pk)
    if question:
        question.delete()
        return HttpResponseRedirect(reverse('moderator:sessionDetails',args=(session_pk,)))

@login_required
@Post_check
def createTopic(request):
    topic = request.POST['topic']
    session_pk = request.POST['session_pk']
    data={
    'topic_name':topic,
    'session':session_pk
    }
    new_topic = TopicSerializer(data=data)
    if new_topic.is_valid():
        new_topic.save()
        session_key=Session.objects.get(id=session_pk).session_key
        current_topic_id = new_topic.data['id']
        qrdata = request.scheme +"://"+request.META['HTTP_HOST']+"/api/"+session_key+"/topic/"+str(current_topic_id)+"/comments/"
        # print(qrdata)
        (newqr,name) = Makeqrfrom(session_key,qrdata)
        (prs, presentation_name) = mtp(current_topic_id)
        if newqr is not None:
            new_topic_instance = new_topic.data
            new_topic_instance['qr_link_name'] = name
            new_topic_instance['presentation_name'] = presentation_name if presentation_name is not None else "null"
            del new_topic_instance['id']
            current_topic = Topic.objects.get(id=current_topic_id)
            updated_topic = updateTopic(current_topic,new_topic_instance)
            if updated_topic:
                return HttpResponseRedirect(reverse('moderator:categorycreate',args=(session_pk,)))
    return HttpResponseRedirect(reverse('moderator:categorycreate',args=(session_pk,)))

def get_topic(pk):
    topic = None
    try:
        topic = Topic.objects.get(id=pk)
    except Topic.DoesNotExist:
        return False
    else:
        return topic

def get_Question(pk):
    question = None
    try:
        question = Question.objects.get(id=pk)
    except Question.DoesNotExist:
        return False
    else:
        return question

def updateTopic(topic_instance,new_topic_instance):
    updated_topic = TopicSerializer(topic_instance,data=new_topic_instance)
    if updated_topic.is_valid():
        updated_topic.save()
        return updated_topic
    return False

def updateQuestion(new_question_instance):
    updated_question = new_question_instance.save()
    return True

@login_required
@Post_check
def createQuestion(request):
    question_id = None
    question = request.POST['question']
    session = request.POST['session_pk']
    option_type = request.POST['option_type']
    question_data = {
    'option_type':option_type,
    'question':question,
    'session':session
    }
    new_question = QuestionSerializer(data=question_data)
    if new_question.is_valid():
        new_question.save()
        question_id = new_question.data['id']
        return HttpResponseRedirect(reverse('moderator:createOptionsIndex', args=(question_id,)))

@login_required
@Get_check
def createOptionsIndex(request,question_pk):
    question = get_Question(question_pk)
    if question:
        context={}
        context['question_pk'] = question_pk
        context['question'] = question.question
        context['type'] = question.option_type
        return render(request,'moderator/createoptions.html',context)
    raise Exception("404")

@login_required
@Post_check
def createOptions(request):
    postdata = request.POST
    options = postdata.getlist('options[]')
    question_id = postdata['question_pk']
    success = True
    for option in options:
        optionData = {
        'question':question_id,
        'option':option
        }
        new_option = OptionSerializer(data=optionData)
        if new_option.is_valid():
            new_option.save()
        else:
            success = False
    if success:
        question = get_Question(question_id)
        if question:
            session_key = question.session.session_key
            qrdata = request.scheme+"://"+request.META['HTTP_HOST']+"/api/"+session_key+"/question/"+str(question_id)+"/options/"
            (newqr,name) = Makeqrfrom(session_key,qrdata)
            (prs, presentation_name) =  mqp(question_id)
            if newqr is not None:
                question.qr_link_name = name
                question.presentation_name = presentation_name if presentation_name is not None else "null"
                updated_question = updateQuestion(question)
                if updated_question:
                    session_pk = question.session.id
                    return HttpResponseRedirect(reverse('moderator:categorycreate',args=(session_pk,)))
        return HttpResponseRedirect(reverse('moderator:createOptionsIndex', args=(question_id,)))
