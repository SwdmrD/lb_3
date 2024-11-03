# Generated by Django 4.2.5 on 2023-10-22 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_fabric_destiny'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='breathability',
            field=models.CharField(choices=[('low', 'Низька'), ('almost absent', 'Майже відсутня'), ('medium', 'Середня'), ('high', 'Висока')], max_length=30, verbose_name='Повітропроникність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='color_fastness',
            field=models.CharField(choices=[('high fastness', 'Висока стійкість'), ('medium fastness', 'Середня стійкість'), ('low fastness', 'Низька стійкість'), ('specialized fastness', 'Спеціалізована стійкість'), ('dyed', 'Фарбована'), ('unknown', 'Невідомо')], max_length=30, verbose_name='Стійкість кольору'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='compression_resistance',
            field=models.CharField(choices=[('high resistance', 'Висока стійкість'), ('medium resistance', 'Середня стійкість'), ('low resistance', 'Низька стійкість'), ('anti-compression fabric', 'Антикомпресійна тканина')], max_length=30, verbose_name='Стійкість до стиснення'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='elasticity',
            field=models.CharField(choices=[('non-elastic', 'Не еластична'), ('almost non-elastic', 'Майже не еластична'), ('partially elastic', 'Частково еластична'), ('highly elastic', 'Добре еластична')], max_length=30, verbose_name='Еластичність'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='surface_texture',
            field=models.CharField(choices=[('glossy', 'Блискуча'), ('geometric', 'Геометрична'), ('smooth', 'Гладка'), ('textured', 'Гофрована'), ('diagonal', 'Діагональна'), ('matte', 'Матова'), ('embossed', 'Рельєфна'), ('ribbed', 'Рубчаста'), ('mesh', 'Сітчаста'), ('complex', 'Складна'), ('striped', 'Смужкова'), ('rough', 'Шорстка')], max_length=30, verbose_name='Текстура'),
        ),
    ]