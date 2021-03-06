# Generated by Django 4.0.4 on 2022-05-13 20:36

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
                ('codi', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'biblioteca',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('codi_barres', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'material',
            },
        ),
        migrations.CreateModel(
            name='Accesori',
            fields=[
                ('codi_barres_accesori', models.OneToOneField(db_column='codi_barres', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca_barcelona.material')),
                ('tipus', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'accesori',
            },
            bases=('biblioteca_barcelona.material',),
        ),
        migrations.CreateModel(
            name='Llibre',
            fields=[
                ('codi_barres_material', models.OneToOneField(db_column='codi_barres', on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='biblioteca_barcelona.material')),
                ('autor', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'llibre',
            },
            bases=('biblioteca_barcelona.material',),
        ),
        migrations.CreateModel(
            name='Soci',
            fields=[
                ('dni', models.CharField(max_length=9, primary_key=True, serialize=False)),
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
                ('quantitat_disponible', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('quantitat_total', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('biblioteca', models.ForeignKey(db_column='biblioteca', on_delete=django.db.models.deletion.CASCADE, related_name='quantitats', to='biblioteca_barcelona.biblioteca')),
                ('material', models.ForeignKey(db_column='material', on_delete=django.db.models.deletion.CASCADE, related_name='quantitats', to='biblioteca_barcelona.material')),
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
                ('data', models.DateField(primary_key=True, serialize=False)),
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
                ('codi', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('biblioteca', models.OneToOneField(db_column='biblioteca', on_delete=django.db.models.deletion.RESTRICT, related_name='codi_postal', to='biblioteca_barcelona.biblioteca')),
            ],
            options={
                'db_table': 'codipostal',
            },
        ),
        migrations.AddField(
            model_name='biblioteca',
            name='materials',
            field=models.ManyToManyField(related_name='biblioteques', through='biblioteca_barcelona.Quantitzacio', to='biblioteca_barcelona.material'),
        ),
    ]
