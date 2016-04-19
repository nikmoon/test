# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0004_auto_20160415_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('etype', models.IntegerField()),
                ('dtstamp', models.DateTimeField(auto_now_add=True)),
                ('lobby', models.ForeignKey(to='lobbyapp.Lobby', null=True)),
                ('user', models.ForeignKey(to='lobbyapp.LobbyUser', null=True)),
            ],
        ),
    ]
