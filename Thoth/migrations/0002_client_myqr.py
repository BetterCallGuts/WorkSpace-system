# Generated by Django 5.0 on 2024-01-01 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thoth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='myqr',
            field=models.ImageField(blank=True, editable=False, upload_to='clientqrcodes'),
        ),
    ]
