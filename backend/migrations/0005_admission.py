# Generated by Django 4.2.16 on 2024-12-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('course', models.CharField(choices=[('full_stack', 'Full-Stack Development'), ('data_science', 'Data Science'), ('web_design', 'Web Design'), ('cyber_security', 'Cyber Security')], max_length=50, verbose_name='Selected Course')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Additional Information')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='Submission Date')),
            ],
        ),
    ]
