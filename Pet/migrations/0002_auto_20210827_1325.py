# Generated by Django 2.2 on 2021-08-27 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petinfo',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]