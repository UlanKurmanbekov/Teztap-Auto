# Generated by Django 5.1.3 on 2024-12-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='car_body',
            field=models.CharField(max_length=255, verbose_name='Кузов'),
        ),
        migrations.AlterField(
            model_name='order',
            name='car_make',
            field=models.CharField(max_length=255, verbose_name='Марка'),
        ),
    ]