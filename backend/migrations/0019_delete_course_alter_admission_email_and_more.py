# Generated by Django 4.2.16 on 2025-01-12 06:48

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0018_admission_created_by_user_id_admission_created_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.AlterField(
            model_name='admission',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='admission',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IN', verbose_name='Phone Number'),
        ),
    ]
