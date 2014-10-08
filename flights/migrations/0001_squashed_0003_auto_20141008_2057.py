# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [('flights', '0001_initial'), ('flights', '0002_auto_20141008_2046'), ('flights', '0003_auto_20141008_2057')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('start_airport', models.CharField(max_length=4)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('end_airport', models.CharField(max_length=4)),
                ('airline', models.CharField(max_length=4)),
                ('flight_number', models.IntegerField()),
                ('distance', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='segment',
            name='trip',
            field=models.ForeignKey(to='flights.Trip'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='segment',
            old_name='distance',
            new_name='distance_miles',
        ),
        migrations.AddField(
            model_name='segment',
            name='duration_mins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='segment',
            name='airline',
            field=models.CharField(max_length=40),
        ),
    ]
