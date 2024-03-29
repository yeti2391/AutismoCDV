# Generated by Django 3.1.2 on 2020-10-25 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('thumbnail', models.ImageField(upload_to='courseThumbnails/')),
                ('publish_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='productsThumbnails', verbose_name='Imagen')),
                ('price', models.FloatField()),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('digital', models.BooleanField(default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', models.FileField(null=True, upload_to='courseVideos', verbose_name='videos de curso')),
                ('title', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='content.course')),
            ],
        ),
    ]
