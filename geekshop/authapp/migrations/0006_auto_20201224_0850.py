# Generated by Django 3.1.3 on 2020-12-24 08:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_auto_20201224_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='avatar',
            field=models.CharField(blank=True, max_length=128, verbose_name='аватар'),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 26, 8, 50, 32, 628638, tzinfo=utc)),
        ),
    ]
