# Generated by Django 2.1.5 on 2019-03-11 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hops_app', '0016_auto_20190225_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='opinto_vuodet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opintovuosi', models.IntegerField(null=True)),
                ('opiskelija', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
