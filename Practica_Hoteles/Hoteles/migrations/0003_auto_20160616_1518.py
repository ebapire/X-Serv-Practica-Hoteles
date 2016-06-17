# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0002_auto_20160616_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='Date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
