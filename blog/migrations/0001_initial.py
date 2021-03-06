# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-16 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('create_data', models.DateField(blank=True)),
                ('change_data', models.DateField(blank=True)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
    ]
