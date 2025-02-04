# Generated by Django 4.2.16 on 2025-01-12 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0020_alter_admission_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
    ]
