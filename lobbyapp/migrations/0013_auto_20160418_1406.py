# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0012_lobby_curr_users_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobbyuser',
            name='lobby',
            field=models.ForeignKey(to='lobbyapp.Lobby'),
        ),
    ]
