# Generated by Django 5.0 on 2024-09-27 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_account_name_account_cheque_account_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
