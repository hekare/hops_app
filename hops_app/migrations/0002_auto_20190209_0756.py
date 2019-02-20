# Generated by Django 2.1.5 on 2019-02-09 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hops_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opintojaksot',
            name='id',
        ),
        migrations.RemoveField(
            model_name='oppi_aineet',
            name='id',
        ),
        migrations.RemoveField(
            model_name='periodit',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tutkinto_ohjelmat',
            name='id',
        ),
        migrations.AlterField(
            model_name='opintojaksot',
            name='tunniste',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='oppi_aineet',
            name='koodi',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='periodit',
            name='opintojakso',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tutkinto_ohjelmat',
            name='koodi',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
