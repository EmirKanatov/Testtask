# Generated by Django 4.1.5 on 2023-01-12 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_manga_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='manga',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='review', to='main.manga'),
        ),
    ]