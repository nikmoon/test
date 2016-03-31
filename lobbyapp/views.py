from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from lobby import settings
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    context = RequestContext(request, {
        'user': request.user,
    })
    return render(request, 'lobbyapp/index.html', context)


def registration(request):
    return HttpResponse('Здесь у нас будет страничка регистрации. Загляните позже...')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'lobbyapp/login.html', RequestContext(request, {
            'form': AuthenticationForm(request),
            'next': request.GET['next'],
        }))
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'lobbyapp/login.html', RequestContext(request, {
                'form': AuthenticationForm(request),
                'next': request.POST['next'] or '/',
            }))
        else:
            login(request, user)
            return HttpResponseRedirect(request.POST['next'])
    else:
        return HttpResponseBadRequest('request method {} not allowed'.format(request.method))



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET['next'] or '/')


