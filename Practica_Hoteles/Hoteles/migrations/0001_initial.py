# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('User', models.CharField(max_length=32)),
                ('Date', models.DateField()),
                ('body', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CSS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('User', models.CharField(max_length=32)),
                ('Letra', models.IntegerField()),
                ('Color', models.CharField(default=b'black', max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre', models.CharField(max_length=32)),
                ('Categ', models.CharField(max_length=32)),
                ('SubCateg', models.IntegerField()),
                ('Descrip', models.TextField(default=b'')),
                ('Direccion', models.TextField(default=b'')),
                ('Url', models.TextField()),
                ('telefono', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hotel_selecc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('User', models.CharField(max_length=32)),
                ('Hotel_id', models.ForeignKey(to='Hoteles.Hotel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Url', models.TextField()),
                ('Hotel_id', models.ForeignKey(to='Hoteles.Hotel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('User', models.CharField(max_length=32)),
                ('body', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comentario',
            name='Hotel_id',
            field=models.ForeignKey(to='Hoteles.Hotel'),
            preserve_default=True,
        ),
    ]
