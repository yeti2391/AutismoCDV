# Generated by Django 3.1.2 on 2020-10-22 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        ('paypal', '0005_auto_20201022_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='productos',
            field=models.ManyToManyField(blank=True, null=True, to='content.Product'),
        ),
    ]
