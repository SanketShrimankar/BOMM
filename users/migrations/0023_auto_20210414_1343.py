# Generated by Django 3.1.7 on 2021-04-14 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20210414_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]