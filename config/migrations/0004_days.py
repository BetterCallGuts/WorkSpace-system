# Generated by Django 3.2.3 on 2023-11-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=255, verbose_name='Day Name')),
            ],
        ),
    ]
