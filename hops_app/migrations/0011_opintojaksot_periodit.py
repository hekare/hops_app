# Generated by Django 2.1.5 on 2019-02-24 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hops_app', '0010_auto_20190223_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='opintojaksot',
            name='periodit',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
