# Generated by Django 4.0.3 on 2022-05-28 17:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_alter_profile_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_url',
            field=models.CharField(blank=True, default='Brak informacji', max_length=200, validators=[django.core.validators.RegexValidator(message='Podaj link do githuba!', regex='^(http(s?):\\/\\/)?(www\\.)?github\\.([a-z])+\\/([A-Za-z0-9]{1,})+\\/?$')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message='Numer telefonu musi być zapisany we formacie: +123456789 ', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]