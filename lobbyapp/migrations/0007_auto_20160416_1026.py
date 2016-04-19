# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0006_auto_20160416_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onlineuser',
            old_name='user',
            new_name='djuser',
        ),
        migrations.AlterField(
            model_name='onlineuser',
            name='last_event_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
