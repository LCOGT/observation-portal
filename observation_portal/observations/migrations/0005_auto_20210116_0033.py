# Generated by Django 2.2.12 on 2021-01-16 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0004_observation_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurationstatus',
            name='state',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('ATTEMPTED', 'ATTEMPTED'), ('NOT_ATTEMPTED', 'NOT_ATTEMPTED'), ('COMPLETED', 'COMPLETED'), ('FAILED', 'FAILED')], default='PENDING', help_text='Current state of this Configuration Status', max_length=40),
        ),
        migrations.AlterField(
            model_name='observation',
            name='state',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('IN_PROGRESS', 'IN_PROGRESS'), ('NOT_ATTEMPTED', 'NOT_ATTEMPTED'), ('COMPLETED', 'COMPLETED'), ('CANCELED', 'CANCELED'), ('ABORTED', 'ABORTED'), ('FAILED', 'FAILED')], db_index=True, default='PENDING', help_text='Current State of this Observation', max_length=40),
        ),
    ]