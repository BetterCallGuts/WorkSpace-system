# Generated by Django 3.2.3 on 2023-11-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thoth', '0036_auto_20231113_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='absent',
            name='Reson',
            field=models.TextField(blank=True, default=' ', verbose_name='reason'),
        ),
    ]
