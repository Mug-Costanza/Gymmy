# Generated by Django 4.2.2 on 2024-03-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0007_alter_workout_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
