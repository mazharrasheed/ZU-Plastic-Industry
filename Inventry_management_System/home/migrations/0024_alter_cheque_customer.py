# Generated by Django 5.0 on 2024-09-08 15:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_cheque_bank_name_alter_cheque_cheque_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='home.customer'),
        ),
    ]