# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-20 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0009_auto_20170620_0323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='info',
            field=models.CharField(max_length=10000),
        ),
    ]