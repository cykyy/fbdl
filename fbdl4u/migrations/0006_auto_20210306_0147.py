# Generated by Django 3.1.6 on 2021-03-06 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fbdl4u', '0005_auto_20210306_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='ip_addr',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='user_agent',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
