from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LobbyUser(models.Model):
    django_user = models.ForeignKey(User)
    deserter_end = models.DateTimeField(null=True)


class Lobby(models.Model):
    USERS_COUNT = (
        (2, '2 игрока'),
        (4, '4 игрока'),
    )
    STATUS = (
        ('WAIT', 'набор участников'),
        ('RUN', 'идет игра')
    )
    max_users_count = models.IntegerField(choices=USERS_COUNT)
    curr_users_count = models.IntegerField()
    owner = models.ForeignKey(LobbyUser)
    name = models.CharField(max_length=200)
    curr_status = models.CharField(max_length=10)
    stop_time = models.DateTimeField(null=True)







