# Generated by Django 5.1.2 on 2024-11-03 10:04

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "lifetime",
            "0002_lifetime_country_lifetime_death_date_lifetime_name_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="week",
        ),
        migrations.AddField(
            model_name="event",
            name="date",
            field=models.DateField(default=datetime.date(1970, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="event",
            name="lifetime",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="lifetime.lifetime",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="Week",
        ),
    ]
