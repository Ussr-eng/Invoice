# Generated by Django 3.1.7 on 2021-04-17 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20210418_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='drop_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(),
        ),
    ]