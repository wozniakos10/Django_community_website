# Generated by Django 4.0.3 on 2022-03-12 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msagh_website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='admin_aproved',
            field=models.BooleanField(default=False),
        ),
    ]
