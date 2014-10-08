# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_squashed_0003_auto_20141008_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='end_city',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='segment',
            name='end_ltlng',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='segment',
            name='start_city',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='segment',
            name='start_ltlng',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
