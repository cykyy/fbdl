# Generated by Django 3.1.6 on 2021-03-06 01:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fbdl4u', '0003_auto_20210306_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
