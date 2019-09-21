# Generated by Django 2.1 on 2018-08-19 09:33

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0026_auto_20180819_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competence',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competence',
            name='name',
            field=models.CharField(default=1, max_length=256, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competence',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='smart_contract.Competence'),
        ),
        migrations.AddField(
            model_name='competence',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competence',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
    ]