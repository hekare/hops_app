# Generated by Django 2.1.5 on 2019-03-12 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hops_app', '0017_opinto_vuodet'),
    ]

    operations = [
        migrations.CreateModel(
            name='toteutukset',
            fields=[
                ('tunniste', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('periodit', models.CharField(max_length=3, null=True)),
                ('aloituspvm', models.CharField(max_length=10, null=True)),
                ('lopetuspvm', models.CharField(max_length=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'Opintojaksojen toteutukset',
            },
        ),
        migrations.AlterModelOptions(
            name='opinto_vuodet',
            options={'verbose_name_plural': 'Opinto vuodet'},
        ),
        migrations.RemoveField(
            model_name='opintojaksot',
            name='periodit',
        ),
        migrations.RemoveField(
            model_name='opintojaksot',
            name='tunniste',
        ),
        migrations.AlterField(
            model_name='opintojaksot',
            name='koodi',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='toteutukset',
            name='koodi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hops_app.opintojaksot'),
        ),
    ]