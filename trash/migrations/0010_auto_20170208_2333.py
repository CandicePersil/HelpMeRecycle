# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-08 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trash', '0009_auto_20161130_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='trashbin',
            name='avatar_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='trashbin',
            name='common_location',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='trashbin',
            name='not_included',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='trashbin',
            name='state_of_items',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
