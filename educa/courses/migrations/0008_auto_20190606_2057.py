# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20190606_2029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='module',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='text',
            old_name='text',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='courses_enrolled', to=settings.AUTH_USER_MODEL),
        ),
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
            model_name='module',
            name='description',
            field=models.TextField(blank=True),
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
