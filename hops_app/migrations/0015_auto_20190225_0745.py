# Generated by Django 2.1.5 on 2019-02-25 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hops_app', '0014_auto_20190225_0738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='valitut_kurssit',
            name='perusopinnot',
        ),
        migrations.RemoveField(
            model_name='valitut_kurssit',
            name='pääaine',
        ),
        migrations.RemoveField(
            model_name='valitut_kurssit',
            name='sivuaine',
        ),
        migrations.AddField(
            model_name='valitut_kurssit',
            name='opintokokonaisuus',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
