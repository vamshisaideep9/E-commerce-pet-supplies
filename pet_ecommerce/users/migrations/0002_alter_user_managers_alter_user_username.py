# Generated by Django 5.1.7 on 2025-03-14 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
