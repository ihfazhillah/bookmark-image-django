# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='target_ct',
            field=models.ForeignKey(blank=True, null=True, related_name='target_obj', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='action',
            name='target_id',
            field=models.PositiveIntegerField(blank=True, null=True, db_index=True),
        ),
    ]
