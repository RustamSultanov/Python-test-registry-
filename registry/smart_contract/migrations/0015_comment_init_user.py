# Generated by Django 2.0.7 on 2018-07-24 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smart_contract', '0014_auto_20180724_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='init_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='init_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
