# Generated by Django 5.0.4 on 2024-05-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(default=False, max_length=50),
        ),
    ]
