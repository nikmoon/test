from django.db import IntegrityError
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sessions.models import Session
from lobbyapp.models import LobbyUser, Lobby

Session.objects.all().delete()
LobbyUser.objects.all().delete()
#for user in User.objects.all():
#    print(user.username)

# Create your views here.

@login_required
def index(request):
    context = RequestContext(request, {
        'gamers_online': LobbyUser.objects.all(),
    })
    return render(request, 'lobbyapp/index.html', context)


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponse('Вы уже вошли как "{}"'.format(request.user.username))
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError as ex:
            return HttpResponseBadRequest('В форме отсутствуют один или несколько параметров: username, password')
        user = authenticate(username=username, password=password)
        if not user is None:
            try:
                LobbyUser.objects.create(django_user=user)
            except IntegrityError as ex:
                message = 'Извините, пользователь с таким ником уже вошел'
            else:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            message = 'Неверный пароль или несуществующее имя пользователя'
    elif request.method == 'GET':
        message = request.GET.get('message')
    else:
        return HttpResponseBadRequest('request method {} not allowed'.format(request.method))

    context = RequestContext(request, {
#        'form': AuthenticationForm(request),
        'message': message,
    })
    return render(request, 'lobbyapp/login.html', context)


def logout_view(request):
    LobbyUser.objects.get(django_user=request.user).delete()
    logout(request)
    return HttpResponseRedirect('/')


def registration_view(request):
    if request.user.is_authenticated():
        return HttpResponse('Вы уже зарегистрированы и залогинены')
    if request.method == 'POST':
        try:
            regname = request.POST['username']
            regpass1 = request.POST['password1']
            regpass2 = request.POST['password1']
        except KeyError:
            return HttpResponse('В форме отсутствуют один или несколько параметров: username, password1, password2')
        user = User.objects.filter(username=regname)
        if user:
            message = 'Имя занято, пожалуйста, выберите другое'
        elif regpass1 != regpass2:
            message = 'Пароли не совпадают'
        else:
            try:
                User.objects.create_user(username=regname, password=regpass1)
            except ValueError as ex:
                message = 'Поля не могут быть пустыми'
            else:
                return HttpResponseRedirect('/login/?message={}'.format('Учетная запись создана, входите'))
    elif request.method == 'GET':
        message = None
    else:
        return HttpResponseBadRequest('request method {} not allowed'.format(request.method))

    context = RequestContext(request, {
        'form': UserCreationForm(),
        'message': message,
    })
    return render(request, 'lobbyapp/registration.html', context)


@login_required
def create_lobby(request):
    return HttpResponse('Скоро Вы уже сможете создавать свои лобби')

@login_required
def join_lobby(request):
    return HttpResponse('Уже очень скоро Вы сможете присоединяться к другим лобби')

