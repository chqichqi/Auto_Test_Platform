# Generated by Django 3.2.20 on 2023-11-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebUiAtuoTest', '0007_auto_20231104_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webcasestep',
            name='order',
            field=models.IntegerField(error_messages={'unique': '测试步骤序号不连续。'}, verbose_name='步骤'),
        ),
    ]