# Generated by Django 2.2.5 on 2019-09-22 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0031_auto_20181026_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competence',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='competence',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='competence',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
