# Generated by Django 3.2.3 on 2023-11-06 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Thoth', '0004_alter_employee_state_of_marrieg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(blank=True, default=' ', max_length=300, null=True, verbose_name='\tEducational Level'),
        ),
    ]
