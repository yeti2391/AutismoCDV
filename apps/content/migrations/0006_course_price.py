# Generated by Django 3.1.2 on 2020-10-19 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20201018_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
