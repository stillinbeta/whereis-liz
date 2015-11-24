# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0007_remove_trainsegment_distance_miles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainsegment',
            name='end_station',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trainsegment',
            name='start_station',
            field=models.CharField(max_length=100),
        ),
    ]
