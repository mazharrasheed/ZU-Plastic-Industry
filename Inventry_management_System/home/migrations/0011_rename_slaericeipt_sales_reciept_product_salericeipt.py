# Generated by Django 5.0 on 2024-08-30 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_rename_gatepass_sales_reciept_product_slaericeipt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales_reciept_product',
            old_name='slaericeipt',
            new_name='salericeipt',
        ),
    ]