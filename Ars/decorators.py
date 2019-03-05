from .models import Session
from rest_framework.response import Response
from rest_framework import status

def check_session(function):

	def function_wrapper(self,request,session_key,**kwargs):
		try:
			session_status = Session.objects.get(session_key=session_key).status
		except Session.DoesNotExist as e:
			return Response({"session_error":"Session not active"},status=status.HTTP_400_BAD_REQUEST)
		else:
			if session_status=="running":
				return function(self,request,session_key,**kwargs)
			return Response({"session_error":"Session not active"},status=status.HTTP_400_BAD_REQUEST)

	return function_wrapper