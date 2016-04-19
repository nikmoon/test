# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0003_lobbyuser_last_event_request'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lobby',
            old_name='stop_time',
            new_name='end_game',
        ),
        migrations.AlterField(
            model_name='lobby',
            name='curr_status',
            field=models.CharField(max_length=10, choices=[('WAIT', 'набор участников'), ('RUN', 'идет игра')]),
        ),
    ]
