# Generated by Django 5.1.3 on 2024-12-08 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_delete_carmake_alter_orderprice_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CarBody',
        ),
        migrations.AlterModelOptions(
            name='orderimage',
            options={'verbose_name': 'Фотография заказа', 'verbose_name_plural': 'Фотографии заказа'},
        ),
    ]
