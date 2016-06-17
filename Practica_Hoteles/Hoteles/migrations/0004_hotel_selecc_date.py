# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Hoteles', '0003_auto_20160616_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel_selecc',
            name='Date',
            field=models.DateField(default=datetime.datetime(2016, 6, 17, 10, 6, 14, 579604, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
