# Generated by Django 2.0.3 on 2018-03-24 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deucer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=255)),
                ('points', models.IntegerField()),
            ],
            options={
                'managed': True,
                'db_table': 'Deucer',
            },
        ),
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'Establishment',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
            options={
                'managed': True,
                'db_table': 'Feature',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('name', models.CharField(max_length=15, primary_key=True, serialize=False)),
            ],
            options={
                'managed': True,
                'db_table': 'Gender',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('value', models.SmallIntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'managed': True,
                'db_table': 'Rating',
            },
        ),
        migrations.CreateModel(
            name='Restroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField()),
                ('establishment', models.ForeignKey(db_column='establishment', on_delete=django.db.models.deletion.DO_NOTHING, to='deuces_app.Establishment')),
                ('features', models.ManyToManyField(to='deuces_app.Feature')),
                ('gender', models.ForeignKey(db_column='gender', on_delete=django.db.models.deletion.DO_NOTHING, to='deuces_app.Gender')),
            ],
            options={
                'managed': True,
                'db_table': 'Restroom',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('deucer', models.ForeignKey(db_column='deucer', on_delete=django.db.models.deletion.DO_NOTHING, to='deuces_app.Deucer')),
                ('rating', models.ForeignKey(db_column='rating', on_delete=django.db.models.deletion.DO_NOTHING, to='deuces_app.Rating')),
                ('restroom', models.ForeignKey(db_column='restroom', on_delete=django.db.models.deletion.DO_NOTHING, to='deuces_app.Restroom')),
            ],
            options={
                'managed': True,
                'db_table': 'Review',
            },
        ),
    ]
