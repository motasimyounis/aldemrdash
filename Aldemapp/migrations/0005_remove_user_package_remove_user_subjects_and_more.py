# Generated by Django 5.0.6 on 2024-09-04 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Aldemapp', '0004_user_device_fingerprint_alter_deviceinfo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='package',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Package',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
