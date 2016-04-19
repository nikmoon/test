from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class OnlineUser(models.Model):
    djuser = models.OneToOneField(User)
    deserter_end = models.DateTimeField(null=True)
    last_event_id = models.BigIntegerField(null=True)


class Lobby(models.Model):
    USERS_COUNT = (
        (2, _('2 игрока')),
        (4, _('4 игрока')),
    )
    STATUS = (
        ('WAIT', _('набор участников')),
        ('RUN', _('идет игра')),
    )
    max_users_count = models.IntegerField(choices=USERS_COUNT)
    curr_users_count = models.IntegerField(default=0)
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    curr_status = models.CharField(max_length=10, choices=STATUS)
    end_game = models.DateTimeField(null=True)
    was_ended = models.BooleanField(default=False)


class LobbyUser(models.Model):
    djuser = models.OneToOneField(User)
    lobby = models.ForeignKey(Lobby)


class Event(models.Model):
    EVENT_TYPE = (
        (1, _('Игрок вошел')),
        (2, _('Игрок вышел')),
        (3, _('Лобби добавлено')),
        (4, _('Лобби завершено')),
        (5, _('Лобби запущено')),
        (6, _('Игрок присоединился к лобби')),
        (7, _('Игрок покинул лобби')),
    )
    etype = models.IntegerField(choices=EVENT_TYPE)
    dtstamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    lobby = models.ForeignKey(Lobby, null=True)




