# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-23 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_trainingrecordtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='portrait',
            field=models.ImageField(blank=True, max_length=256, null=True, upload_to='volunteers'),
        ),
    ]