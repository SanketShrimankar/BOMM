# Generated by Django 3.1.7 on 2021-03-07 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210306_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='bid',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 7, 19, 50, 39, 826290)),
        ),
    ]
