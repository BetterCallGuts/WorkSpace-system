# Generated by Django 4.2.7 on 2023-11-18 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0008_paymentmethod'),
        ('Thoth', '0046_client_voucher_alter_course_voucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='clintcourses',
            name='the_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='config.level', verbose_name='Level'),
        ),
    ]
