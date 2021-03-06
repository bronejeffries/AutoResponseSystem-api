from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status
from django.shortcuts import render
# from django.db.models import Q
from django.contrib.auth.models import User
from .decorators import check_session
from .models import Session, Submission, Topic, Comment, Question, Option
from .Serializers import UserSerializer, SessionSerializer
from .Serializers import SubmissionSerializer, TopicSerializer
from .Serializers import CommentSerializer, QuestionSerializer
from .Serializers import OptionSerializer
from .Qr import GenerateQrCode
import re
import os
import random

# Create your views here.


class userApiView(APIView):

    # checks for the existance of a user
    def check_user(self, user_email):
        try:
                user = User.objects.get(email=user_email)
                if user:
                    return True

        except User.DoesNotExist:
            return False

    # gets the list of all users
    # @params {Request} request
    # return json response

    def get(self, request):
            queryset = User.objects.all()
            serializer_class = UserSerializer(queryset, many=True)
            return Response(serializer_class.data)

    # creates user
    # @params {Request} request
    # @return json | errors

    def post(self, request):
        if self.check_user(request.data.get('email')):
            return Response({'messages': "Username already taken.", 'code': 0})
        else:
            new_user = UserSerializer(data=request.data)
            if new_user.is_valid():
                new_user.save()
                return Response({'messages': "Registration successful",
                                'code': 1,
                                 'id': new_user.data['id']},
                                status=status.HTTP_201_CREATED)
            return Response({'code': 0, 'response': new_user.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class userDetailApiView(APIView):

        #  """
        # Retrieve, update or delete a user instance.
        # """

        def get_user(self, pk):
            try:
                return User.objects.get(id=pk)
            except User.DoesNotExist:
                return False

        # retrieves a user
        # @params {Request} request {User} User
        # @return User=>json | errors

        def get(self, request, pk):
            user = self.get_user(pk)
            serializer_class = UserSerializer(user) if user else {'data': {}}
            return Response(serializer_class.data)

        # updates a User
        # @params {Request} request {User} User
        # @return User=>json | errors

        def put(self, request, pk):
            user_instance = self.get_user(pk)
            if user_instance:
                updated_instance = UserSerializer(user_instance,
                                                  data=request.data)
                if updated_instance.is_valid():
                    updated_instance.save()
                    return Response(updated_instance.data)
                return Response(updated_instance.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # deletes a user
        # @params {Request} request {user} user
        # @return users=>json | errors

        def delete(self, request, pk):
            user = self.get_user(pk)
            if user.delete():
                return Response({'messages': "deleted successfully"},
                                status=status.HTTP_204_NO_CONTENT)
            return Response({'messages': "action not successful"},
                            status=status.HTTP_400_BAD_REQUEST)


class SessionListView(APIView):
        def get_session_by_key(self, session_key):
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

        # gets all sessions created by all users
        # @params {Request} request
        # return json response

        def get(self, request):
            queryset = Session.objects.all()
            serializer_class = SessionSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        #
        # creates new session by the current user
        # @params {Request} request
        # return json response

        def post(self, request):

            # prevent saving a session name more than once
            # check whether session_key is already taken
            session_key = request.data['session_key']
            session = self.get_session_by_key(session_key)
            if session:
                return Response(SessionSerializer(session).data,
                                status=status.HTTP_200_OK)
            else:
                new_session = SessionSerializer(data=request.data)
                if new_session.is_valid():
                    new_session.save()
                    return Response(new_session.data,
                                    status=status.HTTP_201_CREATED)
                return Response(new_session.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class SessionView(APIView):

        # retrieves the sessions created by the user
        # @params {Request} request {User} pk=>id
        # return json response
        def get(self, request, pk):
            queryset = Session.objects.filter(owner=pk)
            serializer_class = SessionSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class SubmissionView(APIView):
        # retrieves all submissions made
        # @params {Request} request
        # @return json response
        @check_session
        def get(self, request, session_key):
            submissions = Submission.objects.all()
            serializer_class = SubmissionSerializer(submissions, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        # creates a new submission
        # @params {Request} request
        # @return json rsponse

        @check_session
        def post(self, request, session_key):
            new_submission = SubmissionSerializer(data=request.data)
            if new_submission.is_valid():
                new_submission.save()
                return Response({'response': new_submission.data},
                                status=status.HTTP_201_CREATED)
            return Response(new_submission.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class SessionSubmissionview(APIView):

        # retrieves all submissions made in a sesion
        # @params {Request} request {Session} session
        # @return json response

        @check_session
        def get(self, request, session_key, session_pk):
            session = Session.get(id=session_pk)
            submissions = session.submission_set.all()
            serializer_class = SubmissionSerializer(submissions, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)


class SubmissionDetailsView(APIView):
        def get_submission(self, pk):
            try:
                submission = Submission.objects.get(id=pk)
            except Submission.DoesNotExist:
                return False
            else:
                return submission

        # retrieves the specific submission url
        # @params {Request} request {Submission} pk
        # @returns json response

        @check_session
        def get(self, request, session_key, pk):
            submission = self.get_submission(pk)
            if submission:
                return Response({'file_url': submission.file_upload.url},
                                status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # deletes a specific file
        # @params {Request} request {submission} pk
        # @returns  json progress message

        @check_session
        def delete(self, request, session_key, pk):
            submission = self.get_submission(pk)
            if submission:
                if submission.delete():
                    return Response({'message': 'Deleted successfully'},
                                    status=status.HTTP_204_NO_CONTENT)
                return Response({'message': 'Something went wrong'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Can not delete file'},
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionsView(APIView):

        # retrieves all questions created by the users
        # @params {Request} request
        # @return json response

        @check_session
        def get(self, request, session_key):
            queryset = Question.objects.all()
            serializer_class = QuestionSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        # creates new question
        # @params {Request} request
        # @return json response

        @check_session
        def post(self, request, session_key):
            new_question = QuestionSerializer(data=request.data)
            if new_question.is_valid():
                new_question.save()
                return Response(new_question.data,
                                status=status.HTTP_201_CREATED)
            return Response(new_question.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class QuestionsDetailView(APIView):

    def get_question(self, pk):
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return False
        else:
            return question

    # retrieves a specific question
    # @params {Request} request {Question} question
    # @return json response

    @check_session
    def get(self, request, session_key, pk):
        queryset = self.get_question(pk)
        if queryset:
            serializer_class = QuestionSerializer(queryset)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @check_session
    def put(self, request, session_key, pk):
        question = self.get_question(pk)
        if question:
            updatequestion = QuestionSerializer(question,
                                                data=request.data)
            if updatequestion.is_valid():
                updatequestion.save()
                return Response(updatequestion.data,
                                status=status.HTTP_200_OK)
            return Response(updatequestion.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "question not found"},
                        status=status.HTTP_400_BAD_REQUEST)


class OptionsView(APIView):

    # retrieves all options
    # @params {Request} request
    # @returns json response

    @check_session
    def get(self, request, session_key):
        options = Option.objects.all()
        serializer_class = OptionSerializer(options, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    # creates new option
    # @params {Request} request
    # @returns json created instance

    @check_session
    def post(self, request, session_key):
        new_option = OptionSerializer(data=request.data)
        if new_option.is_valid():
            new_option.save()
            return Response(new_option.data, status=status.HTTP_201_CREATED)
        return Response(new_option.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionOptions(APIView):

    # gets the options of the specific question
    # @params {Requset} request {Question} pk
    # @returns json response {Options} if exists

    @check_session
    def get(self, request, session_key, question_pk):
        question = QuestionsDetailView.get_question(self, question_pk)
        if question:
            options = question.option_set.all()
            serializer_class = OptionSerializer(options, many=True)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OptionDetailsView(APIView):

    def get_option(self, pk):
        try:
            option = Option.objects.get(id=pk)
        except Option.DoesNotExist:
            return False
        else:
            return option

    # retrives a specific option
    # @params {Request} request {Option} pk
    # @returns Option json response

    @check_session
    def get(self, request, session_key, pk):
        option = self.get_option(pk)
        if option:
            serializer_class = OptionSerializer(option)
            return Response({'option': serializer_class.data},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # updates the option choices
    # @params {Request} request {Option} pk
    # @returns json updated option

    @check_session
    def put(self, request, session_key, pk):
        option = self.get_option(pk)
        if option:
            option.choices = int(option.choices) + int(1)
            option.save()
            serializer_class = OptionSerializer(option)
            return Response(serializer_class.data,
                            status=status.HTTP_201_CREATED)
        return Response({'message': 'invalid option'},
                        status=status.HTTP_400_BAD_REQUEST)


class CommentsView(APIView):
    # retrieves all comments
    # @params {Request} request
    # @returns json response comments

    @check_session
    def get(self, request, session_key):
        comments = Comment.objects.all()
        serializer_class = CommentSerializer(comments, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    # creates a new comment
    # @params {Request} request
    # @returns json response

    @check_session
    def post(self, request, session_key):
        new_comment = CommentSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save()
            return Response(new_comment.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class QuestionCommentsView(APIView):

    # retrieves all comments to a specific question
    # @params {Request} request {Question} question_pk
    # @returns json response comments
    @check_session
    def get(self, request, session_key, question_pk):
        question = QuestionsDetailView.get_question(self, question_pk)
        if question:
            comments = question.comment_set.all()
            serializer_class = CommentSerializer(comments, many=True)
            return Response({'comments': serializer_class.data},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class TopicDetailView(APIView):

    # retrieves a topic by id
    def get_topic(self,pk):
        try:
            topic = Topic.objects.get(id=pk)
        except Topic.DoesNotExist:
            return False
        else:
            return topic

    # retrieves a specific topic
    # @params {Request} request {Topic} topic_pk
    # @returns JsonResponse topic

    @check_session
    def get(self, request, session_key, topic_pk):
        topic = self.get_topic(topic_pk)
        if topic:
            serializer_class = TopicSerializer(topic)
            return Response(serializer_class.data,
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GenerateQrCodeView(APIView):

    @check_session
    def post(self, request, session_key):
        (newqr,qrname) = Makeqrfrom(session_key,request.data['data'])
        if newqr:
            return Response({"name": qrname, "code": 1},
                            status=status.HTTP_200_OK)
        return Response({"code": 0}, status=status.HTTP_400_BAD_REQUEST)


def generate_random():
    return random.randint(1, 1001)

def Makeqrfrom(session_key, data):
    session_req = re.compile(r'([A-Za-z0-9]+)-([A-Za-z0-9]+)-([A-Za-z0-9]+)')
    ssname = session_req.search(session_key).group(1)
    qrname = ssname + str(generate_random())+"qr_"+str(generate_random())
    return (GenerateQrCode(data, qrname),qrname)


class QrCodeDetails(APIView):
    @check_session
    def get(self, request, session_key, qrname):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storage_path = os.path.join(BASE_DIR, 'Ars/templates/media/qrcodes')
        image_path = os.path.join(storage_path, qrname + '.png')
        qr_code_data = open(image_path, "rb").read()
        return HttpResponse(qr_code_data, content_type="image/png")


class LoginApiView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            logined_user = UserSerializer(user)
            return Response({'message': "Login successful",
                             'code': 1, 'id': logined_user.data['id']})
        else:
            return Response({'message': "wrong credentials", 'code': 0})
