# Generated by Django 5.0.2 on 2024-08-21 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pricewebsiteapp", "0005_favourite"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favourite",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="favourited_by",
                to="pricewebsiteapp.product",
            ),
        ),
    ]
