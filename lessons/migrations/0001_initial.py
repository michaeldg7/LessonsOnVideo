# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoCategory'
        db.create_table(u'lessons_videocategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'lessons', ['VideoCategory'])


    def backwards(self, orm):
        # Deleting model 'VideoCategory'
        db.delete_table(u'lessons_videocategory')


    models = {
        u'lessons.videocategory': {
            'Meta': {'object_name': 'VideoCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['lessons']