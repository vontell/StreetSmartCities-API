# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='analysis',
            field=models.CharField(max_length=254),
        ),
    ]
