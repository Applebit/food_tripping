# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.IntegerField()),
                ('entity_type', models.CharField(max_length=20)),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('unique_id', models.CharField(max_length=20)),
            ],
        ),
    ]
