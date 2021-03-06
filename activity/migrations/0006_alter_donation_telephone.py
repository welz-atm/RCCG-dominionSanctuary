# Generated by Django 3.2.5 on 2021-08-04 13:19

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_donation_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='telephone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='E.g. +234 803 123 4567', max_length=128, region=None),
        ),
    ]
