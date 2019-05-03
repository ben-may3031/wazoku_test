# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
        ),
        migrations.CreateModel(
            name='IdeaTfidfWeights',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idea', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idea_tfidf_weights', to='central.Idea')),
                ('tfidfs', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('similarity', models.FloatField(default=0)),
                ('idea_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations_as_idea_1', to='central.Idea')),
                ('idea_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations_as_idea_2', to='central.Idea')),
            ],
        ),
    ]
