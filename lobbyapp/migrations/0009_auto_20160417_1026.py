# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('lobbyapp', '0008_auto_20160416_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineuser',
            name='djuser',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
