# Generated by Django 2.2 on 2021-08-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pet', '0006_auto_20210827_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petinfo',
            name='pet_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]