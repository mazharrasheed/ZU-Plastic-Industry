# Generated by Django 5.0 on 2024-10-06 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_product_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(default='Nos', max_length=255),
        ),
    ]
