# Generated by Django 4.2 on 2023-05-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_closed',
            field=models.BooleanField(null=True),
        ),
    ]
