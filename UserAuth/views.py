from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Ars.decorators import Get_check
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Ars.Serializers import UserSerializer
from rest_framework import status
# Create your views here.

def index(request):
	if request.method=='GET':
		context = {}
		return render(request,"UserAuth/index.html",context)

	elif request.method=='POST':
		context={}
		username=request.POST['username']
		password=request.POST['password']

		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect(reverse('moderator:index'))
		else:
			return render(request,"UserAuth/index.html",context,status=status.HTTP_400_BAD_REQUEST)


def signupview(request):
	if request.method=='GET':
		context={}
		return render(request,"UserAuth/signup.html",context)

	elif request.method == 'POST':
		context={}
		username = request.POST['name']
		email=request.POST['email']
		password = request.POST['password']
		password_confirm = request.POST['re_password']
		if password == password_confirm:
			userdata={
					'username':username,
					'email':email,
					'password':password
			}
			serializer_class = UserSerializer(data=userdata)
			if serializer_class.is_valid():
				serializer_class.save()
				print("signup successful!")
				return HttpResponseRedirect(reverse('UserAuth:index'))
			context['errors'] = serializer_class.errors
			print(context)
			return render(request,"UserAuth/signup.html",context)
		return render(request,"UserAuth/signup.html",context)

@Get_check
@login_required
def logoutview(request):
	logout(request)
	return HttpResponseRedirect(reverse('UserAuth:index'))
