# Generated by Django 5.0 on 2024-09-27 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_account_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='firstname',
            new_name='coname',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='lastname',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='suppliers',
            old_name='firstname',
            new_name='coname',
        ),
        migrations.RenameField(
            model_name='suppliers',
            old_name='lastname',
            new_name='name',
        ),
    ]
