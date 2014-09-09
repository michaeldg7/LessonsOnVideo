# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoLesson'
        db.create_table(u'lessons_videolesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('embed_video.fields.EmbedVideoField')(max_length=200)),
        ))
        db.send_create_signal(u'lessons', ['VideoLesson'])


    def backwards(self, orm):
        # Deleting model 'VideoLesson'
        db.delete_table(u'lessons_videolesson')


    models = {
        u'lessons.videocategory': {
            'Meta': {'object_name': 'VideoCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'lessons.videolesson': {
            'Meta': {'object_name': 'VideoLesson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['lessons']