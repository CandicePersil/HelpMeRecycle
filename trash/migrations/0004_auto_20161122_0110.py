# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 23:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trash', '0003_auto_20161122_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trashbin',
            name='trash_loc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trash.TrashGeoLoc'),
        ),
    ]
