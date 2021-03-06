# Generated by Django 3.2.5 on 2021-09-20 16:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_alter_donation_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='service',
            name='video',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]
