# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lobbyapp', '0009_auto_20160417_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='LobbyUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('djuser', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('lobby', models.OneToOneField(to='lobbyapp.Lobby')),
            ],
        ),
    ]
