# Generated by Django 3.1.7 on 2021-03-06 13:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210306_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
