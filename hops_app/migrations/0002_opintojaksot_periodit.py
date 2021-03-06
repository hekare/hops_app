# Generated by Django 2.1.5 on 2019-02-20 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hops_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='opintojaksot',
            fields=[
                ('tunniste', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('koodi', models.CharField(max_length=20)),
                ('nimi', models.TextField()),
                ('pisteet_min', models.IntegerField()),
                ('pisteet_max', models.IntegerField()),
                ('tutkinto_ohjelma', models.CharField(max_length=20, null=True)),
                ('oppiaine', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='periodit',
            fields=[
                ('opintojakso', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('periodi1', models.BooleanField(default=False)),
                ('periodi2', models.BooleanField(default=False)),
                ('periodi3', models.BooleanField(default=False)),
                ('periodi4', models.BooleanField(default=False)),
                ('periodi5', models.BooleanField(default=False)),
            ],
        ),
    ]
