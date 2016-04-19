from django.db import models
from django.db.models import fields
from django.contrib.auth.models import User

# Create your models here.

class OnlineUser(models.Model):
    djuser = models.OneToOneField(User)
    deserter_end = models.DateTimeField(null=True)
    last_event_id = models.BigIntegerField(null=True)


class Lobby(models.Model):
    USERS_COUNT = (
        (2, '2 игрока'),
        (4, '4 игрока'),
    )
    STATUS = (
        ('WAIT', 'набор участников'),
        ('RUN', 'идет игра'),
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
        (1, 'Игрок вошел'),
        (2, 'Игрок вышел'),
        (3, 'Лобби добавлено'),
        (4, 'Лобби завершено'),
        (5, 'Лобби запущено'),
        (6, 'Игрок присоединился к лобби'),
        (7, 'Игрок покинул лобби'),
    )
    etype = models.IntegerField(choices=EVENT_TYPE)
    dtstamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True)
    lobby = models.ForeignKey(Lobby, null=True)




