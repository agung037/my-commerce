# Generated by Django 3.2 on 2021-08-01 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210802_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
