# Generated by Django 3.2.3 on 2023-11-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_days'),
        ('Thoth', '0031_alter_employee_edu_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Day_per_week',
            field=models.ManyToManyField(blank=True, related_name='Days', to='config.Days'),
        ),
    ]