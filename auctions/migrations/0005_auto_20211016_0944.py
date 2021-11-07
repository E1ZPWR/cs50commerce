# Generated by Django 3.2.8 on 2021-10-16 09:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_create_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.TextField(blank='Title for the comment', max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 16, 9, 44, 41, 302489, tzinfo=utc)),
        ),
    ]
