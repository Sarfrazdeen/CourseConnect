# Generated by Django 4.2.16 on 2025-01-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_alter_admission_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='admission',
            name='course_duration',
            field=models.CharField(default=1, max_length=100, verbose_name='Course Duration'),
            preserve_default=False,
        ),
    ]
