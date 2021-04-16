# Generated by Django 3.1.7 on 2021-04-04 16:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20210325_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='comment',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=800), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='newuser',
            name='liked_books',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), blank=True, null=True, size=None),
        ),
    ]
