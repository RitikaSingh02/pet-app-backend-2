# Generated by Django 2.2 on 2021-11-12 13:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='date_of_creation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]