# Generated by Django 3.2.3 on 2023-11-07 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_coursetype'),
        ('Thoth', '0017_alter_employee_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='coursetype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.coursetype'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='img',
            field=models.ImageField(blank=True, upload_to='EMP Pic', verbose_name=' '),
        ),
        migrations.DeleteModel(
            name='CourseType',
        ),
    ]