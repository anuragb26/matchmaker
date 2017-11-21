# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_useranswer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useranswer',
            old_name='coworker_answer',
            new_name='their_answer',
        ),
        migrations.RenameField(
            model_name='useranswer',
            old_name='coworker_answer_importance',
            new_name='their_answer_importance',
        ),
    ]
