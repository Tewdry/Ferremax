# Generated by Django 4.2.5 on 2024-07-09 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_state_address_region'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='region',
            new_name='state',
        ),
    ]
