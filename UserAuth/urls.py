from django.conf.urls import  url
from . import views

app_name = 'UserAuth'

urlpatterns=[
		url(r'^$',views.index,name='index'),
		url(r'^signup/$',views.signupview, name='signup'),
		url(r'^logout/$',views.logoutview, name='logout')

]
