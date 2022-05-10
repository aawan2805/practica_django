# Generated by Django 4.0.4 on 2022-05-10 15:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biblioteca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codi', models.CharField(max_length=10, unique=True)),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'biblioteca',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codi_barres', models.CharField(max_length=13, unique=True)),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='Soci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=9, unique=True)),
                ('nom', models.CharField(max_length=50)),
                ('cognom', models.CharField(max_length=50)),
                ('data_naixement', models.DateField()),
                ('biblioteca', models.ForeignKey(db_column='biblioteca', on_delete=django.db.models.deletion.RESTRICT, related_name='socis', to='biblioteca_barcelona.biblioteca')),
            ],
            options={
                'db_table': 'soci',
            },
        ),
        migrations.CreateModel(
            name='Quantitzacio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantitat', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('biblioteca', models.ForeignKey(db_column='biblioteca', on_delete=django.db.models.deletion.CASCADE, to='biblioteca_barcelona.biblioteca')),
                ('material', models.ForeignKey(db_column='material', on_delete=django.db.models.deletion.CASCADE, to='biblioteca_barcelona.material')),
            ],
            options={
                'db_table': 'quantitzacio',
                'unique_together': {('material', 'biblioteca')},
            },
        ),
        migrations.CreateModel(
            name='Prestec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_retorn', models.DateField(blank=True, null=True)),
                ('data_limit', models.DateField()),
                ('data_estimacio', models.DateField(blank=True, null=True)),
                ('material', models.ForeignKey(db_column='material', on_delete=django.db.models.deletion.RESTRICT, related_name='prestecs', to='biblioteca_barcelona.material')),
                ('prestec_demanat', models.ForeignKey(blank=True, db_column='prestec_demanat', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='prestec_prestat', to='biblioteca_barcelona.biblioteca')),
                ('soci', models.ForeignKey(db_column='soci', on_delete=django.db.models.deletion.CASCADE, related_name='prestecs', to='biblioteca_barcelona.soci')),
            ],
            options={
                'db_table': 'prestec',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='quantitats',
            field=models.ManyToManyField(through='biblioteca_barcelona.Quantitzacio', to='biblioteca_barcelona.biblioteca'),
        ),
        migrations.CreateModel(
            name='Llibre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(blank=True, max_length=50, null=True)),
                ('codi_barres', models.ForeignKey(db_column='codi_barres', on_delete=django.db.models.deletion.CASCADE, related_name='llibre', to='biblioteca_barcelona.material', unique=True)),
            ],
            options={
                'db_table': 'llibre',
            },
        ),
        migrations.CreateModel(
            name='Horari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(max_length=10)),
                ('hora_obertura', models.CharField(max_length=2)),
                ('hora_tancament', models.CharField(max_length=2)),
                ('biblioteca', models.ForeignKey(db_column='biblioteca', on_delete=django.db.models.deletion.CASCADE, related_name='horaris', to='biblioteca_barcelona.biblioteca')),
            ],
            options={
                'db_table': 'horari',
            },
        ),
        migrations.CreateModel(
            name='Concurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(unique=True)),
                ('edat_minima', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('biblioteca1', models.ForeignKey(db_column='biblioteca1', on_delete=django.db.models.deletion.RESTRICT, related_name='concursos_bib_1', to='biblioteca_barcelona.biblioteca')),
                ('biblioteca2', models.ForeignKey(db_column='biblioteca2', on_delete=django.db.models.deletion.RESTRICT, related_name='concursos_bib_2', to='biblioteca_barcelona.biblioteca')),
                ('socis', models.ManyToManyField(related_name='concursos', to='biblioteca_barcelona.soci')),
            ],
            options={
                'db_table': 'concurs',
            },
        ),
        migrations.CreateModel(
            name='CodiPostal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codi', models.CharField(max_length=5, unique=True)),
                ('biblioteca', models.OneToOneField(db_column='biblioteca', on_delete=django.db.models.deletion.RESTRICT, related_name='codi_postal', to='biblioteca_barcelona.biblioteca')),
            ],
            options={
                'db_table': 'codipostal',
            },
        ),
        migrations.CreateModel(
            name='Accesori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipus', models.CharField(blank=True, max_length=50, null=True)),
                ('codi_barres', models.ForeignKey(db_column='codi_barra', on_delete=django.db.models.deletion.CASCADE, related_name='accesori', to='biblioteca_barcelona.material', unique=True)),
            ],
            options={
                'db_table': 'accesori',
            },
        ),
    ]