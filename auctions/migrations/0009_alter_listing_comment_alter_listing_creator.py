# Generated by Django 4.2 on 2023-05-23 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_image_alter_listing_publishing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='comment',
            field=models.ManyToManyField(blank=True, null=True, related_name='comments', to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
