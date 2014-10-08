# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
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
    ]
