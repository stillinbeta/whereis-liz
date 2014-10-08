# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_auto_20141008_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='airline',
            field=models.CharField(max_length=40),
        ),
    ]
