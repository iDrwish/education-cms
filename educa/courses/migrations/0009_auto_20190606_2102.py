# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20190606_2057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
