# Generated by Django 2.0.3 on 2018-03-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20180327_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]