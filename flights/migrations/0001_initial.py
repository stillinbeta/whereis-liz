# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
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
    ]
