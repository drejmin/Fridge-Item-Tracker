# Generated by Django 4.2.4 on 2023-08-17 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fridge_app', '0019_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='receipt',
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receipt_image',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='fridge_app.photo'),
        ),
    ]
