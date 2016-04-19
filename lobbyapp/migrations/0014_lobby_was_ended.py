# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0013_auto_20160418_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobby',
            name='was_ended',
            field=models.BooleanField(default=False),
        ),
    ]
