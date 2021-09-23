# Generated by Django 3.2.5 on 2021-07-29 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity', '0002_auto_20210728_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField(max_length=25)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('transaction_date', models.CharField(max_length=15)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(help_text='E.g. +234 803 123 4567', max_length=128, null=True, region=None, unique=True)),
                ('reference', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Tithe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('amount', models.IntegerField()),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=15)),
                ('status', models.CharField(blank=True, max_length=15, null=True)),
                ('transaction_date', models.CharField(max_length=15)),
                ('reference', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]