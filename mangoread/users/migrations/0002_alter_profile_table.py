# Generated by Django 4.1.5 on 2023-01-11 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='profile',
            table='user_profile',
        ),
    ]
