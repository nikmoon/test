# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lobby',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('max_users_count', models.IntegerField(choices=[(2, '2 игрока'), (4, '4 игрока')])),
                ('curr_users_count', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('curr_status', models.CharField(max_length=10)),
                ('stop_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LobbyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('deserter_end', models.DateTimeField(null=True)),
                ('django_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lobby',
            name='owner',
            field=models.ForeignKey(to='lobbyapp.LobbyUser'),
        ),
    ]
