# Generated by Django 4.0.3 on 2022-04-21 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msagh_website', '0009_remove_commentspot_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentspot',
            name='spot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='msagh_website.spot'),
        ),
    ]