# Generated by Django 5.1.1 on 2024-09-17 15:28

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_passwordreset"),
    ]

    operations = [
        migrations.AddField(
            model_name="passwordreset",
            name="expires_at",
            field=models.DateTimeField(default=accounts.models.get_expiration_time),
        ),
    ]
