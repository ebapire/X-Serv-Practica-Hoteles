# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0006_comentario_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='latitude',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name='longitude',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name='zipcode',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
