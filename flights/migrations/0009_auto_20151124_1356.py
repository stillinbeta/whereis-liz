# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0008_auto_20151123_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainsegment',
            name='end_ltlng',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trainsegment',
            name='start_ltlng',
            field=models.CharField(max_length=100),
        ),
    ]
