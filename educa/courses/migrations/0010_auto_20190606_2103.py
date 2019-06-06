# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20190606_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='image',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
