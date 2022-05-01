# Generated by Django 4.0.3 on 2022-04-30 23:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('msagh_website', '0012_rename_memes_commentmeme_meme'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='likes',
            field=models.ManyToManyField(related_name='spot_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]