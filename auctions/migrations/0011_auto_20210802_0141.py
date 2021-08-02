# Generated by Django 3.2 on 2021-08-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210802_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wachlist',
        ),
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to='auctions.Listing'),
        ),
    ]