# Generated by Django 4.2.2 on 2023-07-08 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_cost',
            field=models.FloatField(default=0),
        ),
    ]
