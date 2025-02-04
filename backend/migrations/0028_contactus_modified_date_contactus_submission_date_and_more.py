# Generated by Django 4.2.16 on 2025-01-15 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0027_alter_admission_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='modified_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contactus',
            name='submission_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_contacts', to=settings.AUTH_USER_MODEL),
        ),
    ]
