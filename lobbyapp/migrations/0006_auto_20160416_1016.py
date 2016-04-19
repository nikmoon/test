# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lobbyapp', '0005_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('deserter_end', models.DateTimeField(null=True)),
                ('last_event_id', models.BigIntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='lobbyuser',
            name='django_user',
        ),
        migrations.AlterField(
            model_name='event',
            name='etype',
            field=models.IntegerField(choices=[(1, 'Игрок вошел'), (2, 'Игрок вышел'), (3, 'Лобби добавлено'), (4, 'Лобби завершено'), (5, 'Лобби запущено'), (6, 'Игрок присоединился к лобби'), (7, 'Игрок покинул лобби')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='lobby',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='LobbyUser',
        ),
    ]
