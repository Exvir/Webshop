# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-07-28 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_auto_20190728_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
