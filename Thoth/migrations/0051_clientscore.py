# Generated by Django 4.2.7 on 2023-11-18 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Thoth', '0050_alter_coffee_to_who'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_score', models.IntegerField()),
                ('max_score', models.IntegerField()),
                ('the_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Thoth.course')),
            ],
        ),
    ]
