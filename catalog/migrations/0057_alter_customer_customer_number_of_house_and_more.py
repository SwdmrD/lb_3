# Generated by Django 4.2.5 on 2023-12-26 20:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0056_alter_customer_customer_number_of_house'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_number_of_house',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator(code='invalid_number', message='Введіть число від 1 до 500.', regex='^(500|[1-4]?[0-9]{1,2})$')], verbose_name='Номер будинку'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_passport_code',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_passport', message='Номер паспорта не починається з 0 та містить 10 символів', regex='^[1-9]\\d{9}$')], verbose_name='Код паспорту'),
        ),
    ]