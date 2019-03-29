from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Ars.decorators import Get_check
# Create your views here.


@Get_check
def index(request):
    context = {}
    return render(request, 'moderator/index.html', context)
