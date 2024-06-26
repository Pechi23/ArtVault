# Generated by Django 5.0.6 on 2024-05-13 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gallery", "0005_image_gallery_images"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gallery",
            name="images",
        ),
        migrations.AddField(
            model_name="image",
            name="gallery",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="gallery.gallery",
            ),
        ),
    ]
