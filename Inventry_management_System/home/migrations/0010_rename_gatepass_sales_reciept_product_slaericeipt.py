# Generated by Django 5.0 on 2024-08-30 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_sales_reciept_sales_reciept_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales_reciept_product',
            old_name='gatepass',
            new_name='slaericeipt',
        ),
    ]