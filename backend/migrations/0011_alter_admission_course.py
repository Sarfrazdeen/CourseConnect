# Generated by Django 4.2.16 on 2024-12-12 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_delete_contactform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admission',
            name='course',
            field=models.CharField(choices=[('full_stack', 'Full-Stack Development'), ('data_science', 'Data Science'), ('web_design', 'Web Design'), ('cyber_security', 'Cyber Security'), ('c_plus_plus', 'C++ Programming')], max_length=50, verbose_name='Selected Course'),
        ),
    ]
