# Generated by Django 3.2.3 on 2023-11-07 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Thoth', '0015_alter_coursetype_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('The_amount', models.IntegerField(verbose_name='Amount')),
                ('the_reson', models.TextField(blank=True, null=True, verbose_name='reason')),
                ('img', models.ImageField(blank=True, upload_to='', verbose_name='Picture if there certificate[optional]')),
                ('Emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Thoth.employee')),
            ],
        ),
    ]
