"""ars_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import  url
from Ars.views import userApiView,LoginApiView,userDetailApiView,SessionListView,SessionView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('UserAuth.urls')),
    path('moderator/',include('moderator.urls')),
    path('api/<str:session_key>/',include('Ars.urls')),
    re_path(r'^api/sessions/$',SessionListView.as_view(),name='sessions'),
    re_path(r'^api/sessions/(?P<pk>[0-9]+)/$',SessionView.as_view(),name='sessionsview'),
    re_path(r'^api/users/$',userApiView.as_view(),name='users'),
    re_path(r'^api/users/(?P<pk>[0-9]+)/$',userDetailApiView.as_view(),name='userdetails'),
    re_path(r'^api/login/$',LoginApiView.as_view(),name='login')
]
