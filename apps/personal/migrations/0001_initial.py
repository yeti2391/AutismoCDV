# Generated by Django 3.1.2 on 2020-10-30 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('thumbnail', models.ImageField(upload_to='personalThumbnails/')),
                ('description', models.TextField(blank=True, null=True)),
                ('mail', models.EmailField(blank=True, max_length=100, null=True)),
                ('skills', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personal.personalskill')),
            ],
        ),
    ]
