# Generated by Django 3.1.7 on 2021-03-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210308_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
