# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_zero_timestamp(apps, schema_editor):
    Timestamp = apps.get_model("flights", "TimeStamp")
    Timestamp.objects.create(timestamp=0)


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_auto_20141008_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeStamp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('timestamp', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(add_zero_timestamp),
    ]
