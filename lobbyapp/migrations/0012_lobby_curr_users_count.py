# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0011_remove_lobby_curr_users_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='curr_users_count',
            field=models.IntegerField(default=0),
        ),
    ]
