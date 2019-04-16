from django.conf.urls import url
from . import views,sessionViews, categoryViews, presentationViews

app_name = 'moderator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sessioncreate/$', sessionViews.sessionCreate, name='sessioncreate'),
    url(r'^session/(?P<session_pk>[0-9]+)/delete/$', sessionViews.delete_session, name='sessiondelete'),
    url(r'^session/(?P<session_pk>[0-9]+)/deactivate/$', sessionViews.stop_session, name='sessionstop'),
    url(r'^session/(?P<pk>[0-9]+)/categorycreate/$', sessionViews.categoryIndex, name='categorycreate'),
    url(r'^session/categorycreate/discussion/$', categoryViews.createTopic, name='topic_create'),
    url(r'^session/categorycreate/question/$', categoryViews.createQuestion, name='question_create'),
    url(r'^session/categorycreate/question/(?P<question_pk>[0-9]+)/options/$', categoryViews.createOptionsIndex, name='createOptionsIndex'),
    url(r'^session/categorycreate/question/options/$', categoryViews.createOptions, name='createOptions'),
    url(r'^session/(?P<session_pk>[0-9]+)/details/$', sessionViews.sessionDetails, name='sessionDetails'),
    url(r'^session/(?P<session_pk>[0-9]+)/topic/delete/(?P<pk>[0-9]+)/$', categoryViews.deleteTopic, name='topicDelete'),
    url(r'^session/(?P<session_pk>[0-9]+)/question/delete/(?P<pk>[0-9]+)/$', categoryViews.deleteQuestion, name='questionDelete'),
    url(r'^session/category/presentations/(?P<name>[a-zA-Z0-9_.]+)/$', presentationViews.viewPresentation, name='viewPresentation'),
    url(r'^session/presentations/(?P<name>[a-zA-Z0-9_.]+)/$', presentationViews.getPresentation, name='getPresentation')
]
