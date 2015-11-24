# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_auto_20141129_1313'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainSegment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('start_station', models.CharField(max_length=4)),
                ('start_city', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('start_ltlng', models.CharField(max_length=100)),
                ('end_time', models.DateTimeField()),
                ('end_station', models.CharField(max_length=4)),
                ('end_city', models.CharField(max_length=100)),
                ('end_ltlng', models.CharField(max_length=100)),
                ('train_number', models.IntegerField()),
                ('distance_miles', models.IntegerField(null=True)),
                ('duration_mins', models.IntegerField()),
                ('carrier', models.CharField(max_length=40)),
                ('trip', models.ForeignKey(to='flights.Trip')),
            ],
        ),
    ]
