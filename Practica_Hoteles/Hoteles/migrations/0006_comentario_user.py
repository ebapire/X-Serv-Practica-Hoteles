# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0005_remove_comentario_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='User',
            field=models.CharField(default=b'', max_length=32),
            preserve_default=True,
        ),
    ]
