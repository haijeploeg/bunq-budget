# Generated by Django 3.1.1 on 2020-09-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20200912_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='bunq_api_environment',
            field=models.CharField(blank=True, choices=[('SANDBOX', 'SANDBOX'), ('PRODUCTION', 'PRODUCTION')], max_length=10),
        ),
        migrations.AlterField(
            model_name='settings',
            name='bunq_api_key',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]