# Generated by Django 3.1.7 on 2021-03-08 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210308_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(verbose_name=datetime.datetime(2021, 3, 8, 21, 8, 36, 161450)),
        ),
    ]
