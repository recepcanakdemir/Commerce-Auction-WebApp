# Generated by Django 4.2 on 2023-05-22 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.ManyToManyField(blank=True, related_name='bids', to='auctions.bid'),
        ),
    ]
