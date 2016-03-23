# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 09:02
from __future__ import unicode_literals

from django.db import migrations, models
import mrupload.models
import mrupload.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mrupload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.FileField(max_length=200, upload_to=mrupload.models.mr_upload_location, validators=[mrupload.validators.validate_file_type]),
        ),
    ]
