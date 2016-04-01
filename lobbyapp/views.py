from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session

Session.objects.all().delete()

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        context = RequestContext(request, {
        })
        return render(request, 'lobbyapp/index.html', context)

    else:
        if request.method == 'GET':
            context = RequestContext(request, {
                'form': AuthenticationForm(request),
                'next': request.GET.get('next') or '/',
            })
            return render(request, 'lobbyapp/index.html', context)
        elif request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is None:
                context = RequestContext(request, {
                    'form': AuthenticationForm(request),
                    'next': request.POST['next'] or '/',
                    'fail': True,
                })
                return render(request, 'lobbyapp/index.html', context)
            else:
                login(request, user)
                return HttpResponseRedirect(request.POST['next'])
        else:
            return HttpResponseBadRequest('request method {} not allowed'.format(request.method))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next') or '/')

