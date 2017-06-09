# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('buscador', '0004_auto_20170517_0053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tag', models.CharField(max_length=40)),
            ],
        ),
        migrations.RemoveField(
            model_name='paginadeconfianza',
            name='area',
        ),
        migrations.AddField(
            model_name='area',
            name='paginas_de_confianza',
            field=models.ManyToManyField(to='buscador.PaginaDeConfianza'),
        ),
        migrations.AlterField(
            model_name='paginadeconfianza',
            name='fecha_pagina',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
