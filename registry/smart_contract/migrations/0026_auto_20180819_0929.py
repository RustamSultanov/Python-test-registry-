# Generated by Django 2.1 on 2018-08-19 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0025_auto_20180819_0902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competence',
            name='level',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='competence',
            name='tree_id',
        ),
    ]
