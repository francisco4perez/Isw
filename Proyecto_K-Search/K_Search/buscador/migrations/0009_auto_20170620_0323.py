# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-20 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0008_auto_20170611_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenido',
            name='dominio_fuente',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='contenido',
            name='tags',
            field=models.ManyToManyField(to='buscador.Tags'),
        ),
        migrations.AlterField(
            model_name='contenido',
            name='info',
            field=models.CharField(max_length=5000),
        ),
    ]
