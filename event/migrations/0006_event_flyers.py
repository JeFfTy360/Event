# Generated by Django 5.0.4 on 2024-05-21 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_remove_event_remaining_place_event_sold_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='flyers',
            field=models.ImageField(blank=True, upload_to='uploads'),
        ),
    ]