# Generated by Django 5.1.2 on 2024-11-02 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0060_alter_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='id_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.item', verbose_name='Товар'),
        ),
    ]
