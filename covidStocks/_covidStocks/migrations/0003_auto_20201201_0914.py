# Generated by Django 3.1.2 on 2020-12-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_covidStocks', '0002_auto_20201127_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweets',
            name='date',
            field=models.DateField(),
        ),
    ]
