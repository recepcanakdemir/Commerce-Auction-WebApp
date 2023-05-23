# Generated by Django 4.2 on 2023-05-23 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='publishing_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]