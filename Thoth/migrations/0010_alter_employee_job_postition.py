# Generated by Django 3.2.3 on 2023-11-06 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
        ('Thoth', '0009_alter_employee_job_postition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_postition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='config.jobposition'),
        ),
    ]
