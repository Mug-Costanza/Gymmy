# Generated by Django 4.2.2 on 2024-03-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0008_alter_workout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='duration',
            field=models.DecimalField(decimal_places=0, default=None, max_digits=5, null=True),
        ),
    ]
