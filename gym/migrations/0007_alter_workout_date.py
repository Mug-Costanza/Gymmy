# Generated by Django 4.2.2 on 2024-03-21 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0006_alter_workout_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
