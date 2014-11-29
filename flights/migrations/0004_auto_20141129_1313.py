# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='distance_miles',
            field=models.IntegerField(null=True),
        ),
    ]
