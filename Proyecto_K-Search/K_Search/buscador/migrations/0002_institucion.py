# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_institucion', models.CharField(max_length=100)),
            ],
        ),
    ]
