# Generated by Django 2.1 on 2018-08-19 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0023_comment_adition_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='accept',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='customer_flag',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='failure',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='hide',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='implementer_flag',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='useraccept',
            name='accept',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='useraccept',
            name='failure',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]