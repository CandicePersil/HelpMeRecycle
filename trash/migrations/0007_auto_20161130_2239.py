# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trash', '0006_auto_20161123_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trashitem',
            name='item_img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]