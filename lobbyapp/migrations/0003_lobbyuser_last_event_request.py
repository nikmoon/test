# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0002_auto_20160405_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobbyuser',
            name='last_event_request',
            field=models.DateTimeField(null=True),
        ),
    ]
