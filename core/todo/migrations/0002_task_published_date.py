# Generated by Django 5.1.1 on 2024-09-09 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='published_date',
            field=models.DateTimeField(default='2022:12:12 22:15'),
            preserve_default=False,
        ),
    ]
