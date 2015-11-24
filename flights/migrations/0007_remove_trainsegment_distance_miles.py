# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0006_auto_20151123_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainsegment',
            name='distance_miles',
        ),
    ]
