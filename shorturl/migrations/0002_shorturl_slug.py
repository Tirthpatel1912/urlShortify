# Generated by Django 4.2.16 on 2024-10-23 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shorturl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='slug',
            field=models.SlugField(default=False, unique=True),
        ),
    ]