from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Session(models.Model):
    status = models.CharField(max_length=25, default='running')
    session_key = models.CharField(max_length=250, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)


class Submission(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    file_upload = models.FileField(null=False)


class Topic(models.Model):
    topic_name = models.CharField(max_length=250, null=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    qr_link_name = models.CharField(max_length=25, null=True)    


class Comment(models.Model):
    comment = models.CharField(max_length=350, null=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Question(models.Model):
    option_type = models.CharField(max_length=12, null=True)
    question = models.CharField(max_length=350, null=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    qr_link_name = models.CharField(max_length=25, null=True)


class Option(models.Model):
    option = models.CharField(max_length=350, null=False)
    choices = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Qrcodemodel(models.Model):
    idNo = models.IntegerField(null=False)
    qrImageName = models.CharField(max_length=250, null=False)
    category = models.CharField(max_length=150, null=False)
