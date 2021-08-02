# Generated by Django 3.2 on 2021-08-02 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='price',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
