# Generated by Django 2.1.5 on 2019-02-22 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hops_app', '0008_auto_20190222_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valitut_kurssit',
            name='kurssi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hops_app.opintojaksot'),
        ),
    ]
