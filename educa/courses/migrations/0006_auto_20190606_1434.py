# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='student',
            new_name='students',
        ),
    ]
