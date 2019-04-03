from .models import Session
from rest_framework.response import Response
from rest_framework import status


def check_session(function):
    def function_wrapper(self, request, session_key, **kwargs):
        session_status = None
        try:
            session_status = Session.objects.get(session_key=session_key
                                                 ).status
        except Session.DoesNotExist:
            session_status = None
        except Session.MultipleObjectsReturned:
            session_status = Session.objects.filter(session_key=session_key
                                                    ).last().status
        finally:
            if session_status is not None:
                if session_status == "running":
                    return function(self, request, session_key, **kwargs)
                return Response({"session_error": "Session not active"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"session_error": "Session does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)
    return function_wrapper


def Get_check(function):
    def wrapper(request, **kwargs):
        if request is not None:
            if request.method == "GET":
                return function(request, **kwargs)
            raise Exception("method not allowed.")
        raise Exception("request is null")
    return wrapper

def Del_check(function):
    def wrapper(request, **kwargs):
        if request is not None:
            if request.method == "DELETE":
                return function(request, **kwargs)
            raise Exception("method not allowed.")
        raise Exception("request is null")
    return wrapper


def Post_check(function):
    def wrapper(request, **kwargs):
        if request is not None:
            if request.method == "POST":
                return function(request, **kwargs)
            raise Exception("method not allowed.")
        raise Exception("request is null")
    return wrapper
