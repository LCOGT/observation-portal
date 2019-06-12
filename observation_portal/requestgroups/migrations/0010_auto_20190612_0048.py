# Generated by Django 2.1.5 on 2019-06-12 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requestgroups', '0009_auto_20190518_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='diff_epoch_rate',
        ),
        migrations.RemoveField(
            model_name='target',
            name='diff_pitch_acceleration',
        ),
        migrations.RemoveField(
            model_name='target',
            name='diff_pitch_rate',
        ),
        migrations.RemoveField(
            model_name='target',
            name='diff_roll_acceleration',
        ),
        migrations.RemoveField(
            model_name='target',
            name='diff_roll_rate',
        ),
        migrations.AddField(
            model_name='target',
            name='diff_altitude_acceleration',
            field=models.FloatField(blank=True, help_text='Differential altitude acceleration (arcsec/s^2)', null=True, verbose_name='differential altitude acceleration'),
        ),
        migrations.AddField(
            model_name='target',
            name='diff_altitude_rate',
            field=models.FloatField(blank=True, help_text='Differential altitude rate (arcsec/s)', null=True, verbose_name='differential altitude rate'),
        ),
        migrations.AddField(
            model_name='target',
            name='diff_azimuth_acceleration',
            field=models.FloatField(blank=True, help_text='Differential azimuth acceleration (arcsec/s^2)', null=True, verbose_name='differential azimuth acceleration'),
        ),
        migrations.AddField(
            model_name='target',
            name='diff_azimuth_rate',
            field=models.FloatField(blank=True, help_text='Differential azimuth rate (arcsec/s)', null=True, verbose_name='differential azimuth rate'),
        ),
        migrations.AddField(
            model_name='target',
            name='diff_epoch',
            field=models.FloatField(blank=True, help_text='Reference time for non-sidereal motion (MJD)', null=True, verbose_name='differential epoch'),
        ),
    ]
