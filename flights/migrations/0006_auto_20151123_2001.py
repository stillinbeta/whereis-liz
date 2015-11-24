# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0005_trainsegment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainsegment',
            name='end_ltlng',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='trainsegment',
            name='start_ltlng',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
