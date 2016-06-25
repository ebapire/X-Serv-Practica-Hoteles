# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0007_auto_20160625_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='css',
            name='Letra',
            field=models.CharField(default=b'100%', max_length=32),
            preserve_default=True,
        ),
    ]
