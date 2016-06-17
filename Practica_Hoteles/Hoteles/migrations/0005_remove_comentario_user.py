# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0004_hotel_selecc_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='User',
        ),
    ]
