# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0003_auto_20170419_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='m',
            field=models.IntegerField(default=0),
        ),
    ]
