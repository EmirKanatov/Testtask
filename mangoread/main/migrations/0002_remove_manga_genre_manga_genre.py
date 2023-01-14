# Generated by Django 4.1.5 on 2023-01-12 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manga',
            name='genre',
        ),
        migrations.AddField(
            model_name='manga',
            name='genre',
            field=models.ManyToManyField(related_name='manga', to='main.genre'),
        ),
    ]