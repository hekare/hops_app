# Generated by Django 2.1.5 on 2019-03-13 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hops_app', '0018_auto_20190312_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='valitut_kurssit',
            name='periodi',
        ),
        migrations.AddField(
            model_name='valitut_kurssit',
            name='toteutus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hops_app.toteutukset'),
        ),
    ]
