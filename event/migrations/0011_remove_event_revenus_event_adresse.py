# Generated by Django 5.0.4 on 2024-06-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0010_event_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='revenus',
        ),
        migrations.AddField(
            model_name='event',
            name='adresse',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
