# Generated by Django 3.2.8 on 2021-10-20 02:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 20, 2, 4, 47, 257920, tzinfo=utc)),
        ),
    ]
