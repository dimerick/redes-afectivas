# Generated by Django 2.0 on 2018-01-07 03:12

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('place', models.TextField()),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('num_person', models.PositiveIntegerField()),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('instruments', models.TextField(null=True)),
                ('focus', models.TextField(null=True)),
                ('vos', models.TextField(null=True)),
                ('result', models.TextField(null=True)),
            ],
        ),
    ]
