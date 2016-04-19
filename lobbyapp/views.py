from django.db import IntegrityError
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sessions.models import Session
from lobbyapp.models import OnlineUser, Lobby, LobbyUser, Event
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta
import pytz

Session.objects.all().delete()
OnlineUser.objects.all().delete()
Lobby.objects.all().delete()
LobbyUser.objects.all().delete()
Event.objects.all().delete()
#for user in User.objects.all():
#    print(user.username)

# Create your views here.

@login_required
def index(request):
    online_user = OnlineUser.objects.get(djuser=request.user)
    online_user.last_event_id = Event.objects.all().aggregate(Max('id'))['id__max']

    if online_user.deserter_end:
        if online_user.deserter_end > datetime.now(pytz.utc):
            deserter_left = (online_user.deserter_end - datetime.now(pytz.utc)).seconds
        else:
            deserter_left = None
            online_user.deserter_end
    else:
        deserter_left = None
    online_user.save()

    try:
        lobby_id = LobbyUser.objects.get(djuser=request.user).lobby.id
    except Exception as es:
        lobby_id = None

    context = RequestContext(request, {
        'gamers_online': OnlineUser.objects.all(),
        'lobbys': Lobby.objects.filter(was_ended=False),
        'lobby_id': lobby_id,
        'deserter_left': deserter_left,
    })
    return render(request, 'lobbyapp/index.html', context)


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponse(_('Вы уже вошли как') +  '"{}"'.format(request.user.username))
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError as ex:
            return HttpResponseBadRequest(_('В форме отсутствуют один или несколько параметров: username, password'))
        user = authenticate(username=username, password=password)
        if not user is None:
            try:
                online_user = OnlineUser.objects.create(djuser=user)
            except IntegrityError as ex:
                OnlineUser.objects.get(djuser=user).delete()
                for s in Session.objects.all():
                    if s.get_decoded().get('_auth_user_id') == str(user.id):
                        s.delete()
                online_user = OnlineUser.objects.create(djuser=user)
            login(request, user)
            ev = Event.objects.create(etype=1, user=user)
            online_user.last_event_id = ev.id
            online_user.save()
            return HttpResponseRedirect('/')
        else:
            message = _('Неверный пароль или несуществующее имя пользователя')
    elif request.method == 'GET':
        message = request.GET.get('message')
    else:
        return HttpResponseBadRequest('request method {} not allowed'.format(request.method))

    context = RequestContext(request, {
        'message': message,
    })
    return render(request, 'lobbyapp/login.html', context)


def logout_view(request):
    if request.user.is_authenticated():
        ev = Event.objects.create(etype=2, user=request.user)
        OnlineUser.objects.get(djuser=request.user).delete()
        lobby = Lobby.objects.filter(was_ended=False).filter(owner=request.user)
        if lobby:
            LobbyUser.objects.filter(lobby=lobby[0]).delete()
            ev = Event.objects.create(etype=4, lobby=lobby[0])
            lobby[0].was_ended = True
            lobby[0].save()
        else:
            lobby_user = LobbyUser.objects.filter(djuser=request.user)
            if lobby_user:
                cur_lobby = lobby_user[0].lobby
                Event.objects.create(etype=7, user=request.user, lobby=cur_lobby)
                cur_lobby.curr_users_count -= 1
                cur_lobby.save()
                lobby_user.delete()
        logout(request)
    return HttpResponseRedirect('/')


def registration_view(request):
    if request.user.is_authenticated():
        return HttpResponse(_('Вы уже зарегистрированы и залогинены'))
    if request.method == 'POST':
        try:
            regname = request.POST['username']
            regpass1 = request.POST['password1']
            regpass2 = request.POST['password1']
        except KeyError:
            return HttpResponse(_('В форме отсутствуют один или несколько параметров: username, password1, password2'))
        user = User.objects.filter(username=regname)
        if user:
            message = _('Имя занято, пожалуйста, выберите другое')
        elif regpass1 != regpass2:
            message = _('Пароли не совпадают')
        else:
            try:
                User.objects.create_user(username=regname, password=regpass1)
            except ValueError as ex:
                message = _('Поля не могут быть пустыми')
            else:
                return HttpResponseRedirect('/login/?message={}'.format(_('Учетная запись создана, входите')))
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
def get_new_messages(request):
    runned_lobbys = Lobby.objects.exclude(end_game=None)
    for lobby in runned_lobbys:
        if lobby.end_game < datetime.now(pytz.utc):
            lobby.end_game = None
            lobby.was_ended = True
            lobby.save()
            LobbyUser.objects.filter(lobby=lobby).delete()
            Event.objects.create(etype=4, lobby=lobby)

    online_user = OnlineUser.objects.get(djuser=request.user)
    events = Event.objects.filter(id__gt=online_user.last_event_id).order_by('id')
    d = { 'count': len(events), 'events': {}}
    if events:
        for event in events:
            d['events'][event.id] = {
                'etype': str(event.etype),
            }
            if event.etype in [1, 2]:
                d['events'][event.id]['user'] = str(event.user)
            elif event.etype in [3, 4, 5, 6, 7]:
                d['events'][event.id]['lobby'] = {
                    'id': event.lobby.id,
                    'name': event.lobby.name,
                    'owner': str(event.lobby.owner),
                    'max_users_count': event.lobby.max_users_count,
                    'curr_users_count': event.lobby.curr_users_count,
                    'status': event.lobby.get_curr_status_display(),
                }
                if event.etype in [6, 7]:
                    d['events'][event.id]['user'] = str(event.user)
        online_user.last_event_id = events.aggregate(Max('id'))['id__max']
        online_user.save()
    response = JsonResponse(d)
    return response


@login_required
def create_lobby(request):
    if LobbyUser.objects.filter(djuser=request.user):
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        online_user = OnlineUser.objects.get(djuser=request.user)
        if online_user.deserter_end:
            return HttpResponseRedirect("/")
        context = RequestContext(request, {
            'Lobby': Lobby,
        })
        return render(request, 'lobbyapp/create_lobby.html', context)
    elif request.method == 'POST':
        message = ''
        if not request.POST['name']:
            message = _('Вы не ввели название для нового лобби')
            return render(request, 'lobbyapp/create_lobby.html', RequestContext(request, {
                'Lobby': Lobby,
                'message': message,
            }))
        c = request.POST['count']
        n = request.POST['name']
        lobby = Lobby.objects.create(max_users_count=c, owner=request.user, name=n, curr_status='WAIT')
        LobbyUser.objects.create(djuser=request.user, lobby=lobby)
        lobby.curr_users_count = 1
        lobby.save()
        event = Event.objects.create(etype=3, lobby=lobby)
        online_user = OnlineUser.objects.get(djuser=request.user)
        online_user.last_event_id = event.id
        online_user.save()
        return HttpResponseRedirect('/lobby/')


@login_required
def lobby_view(request):
    try:
        lobby_user = LobbyUser.objects.get(djuser=request.user)
    except ObjectDoesNotExist as ex:
        return HttpResponseRedirect('/')
    lobby = lobby_user.lobby

    if lobby.end_game:
        if lobby.end_game > datetime.now(pytz.utc):
            time_left = (lobby.end_game - datetime.now(pytz.utc)).seconds
    else:
        time_left = None
        if request.method == 'POST':
            if 'begin_game' in request.POST:
                if lobby.curr_users_count == lobby.max_users_count:
                    lobby.curr_status = 'RUN'
                    ev = Event.objects.create(etype=5, lobby=lobby)
                    lobby.end_game = ev.dtstamp + timedelta(minutes=1)
                    lobby.save()
                return HttpResponseRedirect('/lobby/')
            elif 'leave_lobby' in request.POST:
                lobby.curr_users_count -= 1
                lobby.save()
                lobby_user.delete()
                Event.objects.create(etype=7, user=request.user, lobby=lobby)
                online_user = OnlineUser.objects.get(djuser=request.user)
                online_user.deserter_end = datetime.now(pytz.utc) + timedelta(minutes=1)
                online_user.save()
                return HttpResponseRedirect("/")
    gamers = LobbyUser.objects.filter(lobby=lobby)
    context = RequestContext(request, {
        'lobby': lobby,
        'gamers': gamers,
        'count': len(gamers),
        'time_left': time_left,
    })
    return render(request, 'lobbyapp/lobby.html', context)

@login_required
def join_lobby(request, lobby_id):
    try:
        lobby = Lobby.objects.get(id=lobby_id)
    except ObjectDoesNotExist as ex:
        return HttpResponse('Exception')
    if lobby.curr_users_count == lobby.max_users_count:
        return HttpResponseRedirect('/')
    if lobby.curr_status == 'RUN':
        return HttpResponseRedirect('/')
    online_user =  OnlineUser.objects.get(djuser=request.user)
    if online_user.deserter_end:
        if online_user.deserter_end > datetime.now(pytz.utc):
            return HttpResponseRedirect("/")
        else:
            online_user.deserter_end = None
            online_user.save()

    try:
        lobby_user = LobbyUser.objects.create(djuser=request.user, lobby=lobby)
    except IntegrityError as ie:
        return HttpResponseRedirect('/')
    lobby.curr_users_count += 1
    lobby.save()

    ev = Event.objects.create(etype=6, user=request.user, lobby=lobby)

    online_user = OnlineUser.objects.get(djuser=request.user)
    online_user.last_event_id = ev.id
    online_user.save()

    return HttpResponseRedirect('/lobby/')


@login_required
def start_game(request):
    return render(request, 'lobbyapp/game.html')