# Generated by Django 4.2 on 2023-06-14 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_remove_listing_is_in_watchlist_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
