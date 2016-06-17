# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='tot_comentarios',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotel',
            name='SubCateg',
            field=models.CharField(default=b'', max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotel',
            name='telefono',
            field=models.CharField(max_length=32),
            preserve_default=True,
        ),
    ]
