# Generated by Django 5.2.1 on 2025-05-12 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asn_shop', '0002_remove_myuser_groups_remove_myuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
