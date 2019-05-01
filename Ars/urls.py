from django.conf.urls import url
from .views import (SessionListView,
					SessionView,
					QuestionsView,
					QuestionsDetailView,
					SessionSubmissionview,
					SubmissionView,
					SubmissionDetailsView,
					OptionsView,
					QuestionOptions,
					OptionDetailsView,
					CommentsView,
					QuestionCommentsView,
					GenerateQrCodeView,
					QrCodeDetails,
					TopicDetailView)

app_name = 'Ars'

urlpatterns = [

			url(r'^questions/$',QuestionsView.as_view(),name='questions'),
			url(r'^questions/(?P<pk>[0-9]+)/$',QuestionsDetailView.as_view(),name='questionsdetails'),

			url(r'^submissions/$',SubmissionView.as_view(),name='submissioncreate'),
			url(r'^submissions/(?P<session_pk>[0-9]+)/$',SessionSubmissionview.as_view(),name='sessionsubmissions'),
			url(r'^submission/(?P<pk>[0-9]+)/$',SubmissionDetailsView.as_view(),name='submissiondetails'),

			url(r'^options/$',OptionsView.as_view(),name='optionscreate'),
			url(r'^question/(?P<question_pk>[0-9]+)/options/$',QuestionOptions.as_view(),name='question_options'),
			url(r'^option/(?P<pk>[0-9]+)/$',OptionDetailsView.as_view(),name='optionsdetails'),

			url(r'^qrcodes/$', GenerateQrCodeView.as_view(), name='generateqrcode'),
			url(r'^qrcodes/(?P<qrname>[a-zA-Z0-9_.]+)/$', QrCodeDetails.as_view(), name='qrcode_details'),

			url(r'^comments/$',CommentsView.as_view(),name='commentscreate'),
			url(r'^topic/(?P<question_pk>[0-9]+)/comments/$',QuestionCommentsView.as_view(),name='questioncomments'),
			url(r'^topic/(?P<topic_pk>[0-9]+)/$',TopicDetailView.as_view(),name='topic_details')

]
