# Generated by Django 5.0.4 on 2024-05-13 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_ticket_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='remaining_place',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
