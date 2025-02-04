# Generated by Django 4.2.16 on 2025-01-12 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_admission_course_duration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admission',
            options={'ordering': ['-submission_date'], 'verbose_name': 'Admission', 'verbose_name_plural': 'Admissions'},
        ),
        migrations.AlterField(
            model_name='admission',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='Phone Number'),
        ),
    ]
