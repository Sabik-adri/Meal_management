# Generated by Django 5.0.6 on 2024-07-08 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_alter_bazarentry_person_alter_mealentry_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='money_given',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
