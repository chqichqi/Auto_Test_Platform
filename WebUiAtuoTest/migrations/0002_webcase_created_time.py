# Generated by Django 3.2.20 on 2023-09-23 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebUiAtuoTest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcase',
            name='created_time',
            field=models.DateTimeField(auto_now=True, verbose_name='创建时间'),
        ),
    ]
