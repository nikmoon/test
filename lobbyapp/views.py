from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from lobby import settings

# Create your views here.
#@login_required
def index(request):
    return HttpResponse('Hi человеки')
