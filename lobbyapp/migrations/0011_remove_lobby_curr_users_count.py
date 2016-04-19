# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0010_lobbyuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lobby',
            name='curr_users_count',
        ),
    ]
