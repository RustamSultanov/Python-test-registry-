# Generated by Django 2.0.7 on 2018-07-11 20:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smart_contract', '0003_auto_20180711_0416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='recipient_user',
        ),
        migrations.AddField(
            model_name='comment',
            name='recipient_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
