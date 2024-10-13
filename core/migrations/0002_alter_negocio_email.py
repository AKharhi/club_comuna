# Generated by Django 5.1.1 on 2024-10-13 02:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="negocio",
            name="email",
            field=models.EmailField(
                max_length=100, validators=[django.core.validators.EmailValidator()]
            ),
        ),
    ]
