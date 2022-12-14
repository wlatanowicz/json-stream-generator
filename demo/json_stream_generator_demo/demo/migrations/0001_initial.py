# Generated by Django 4.1.2 on 2022-10-09 19:15

from django.db import migrations, models

import demo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Demo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.FloatField(default=demo.models.default_number)),
                (
                    "text",
                    models.CharField(default=demo.models.default_text, max_length=16),
                ),
            ],
        ),
    ]
