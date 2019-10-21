# Generated by Django 2.2.5 on 2019-10-06 08:54

from django.db import migrations, models
import smart_contract.models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0036_auto_20191004_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccept',
            name='biography',
            field=models.TextField(blank=True, verbose_name='Краткая биография'),
        ),
        migrations.AddField(
            model_name='useraccept',
            name='city',
            field=models.CharField(default='Москва', max_length=30, verbose_name='Город проживания'),
        ),
        migrations.AddField(
            model_name='useraccept',
            name='contacts',
            field=models.TextField(blank=True, verbose_name='Контакты'),
        ),
        migrations.AddField(
            model_name='useraccept',
            name='userpic',
            field=models.ImageField(blank=True, null=True, upload_to=smart_contract.models.image_folder, verbose_name='Юзерпик'),
        ),
    ]
