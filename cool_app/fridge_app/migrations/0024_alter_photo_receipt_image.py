# Generated by Django 4.2.4 on 2023-08-17 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fridge_app', '0023_remove_receipt_receipt_image_photo_receipt_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='receipt_image',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='fridge_app.receipt'),
        ),
    ]
