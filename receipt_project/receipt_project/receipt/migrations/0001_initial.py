# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Show'
        db.create_table(u'receipt_show', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Locally Made', max_length=255)),
            ('info', self.gf('django.db.models.fields.TextField')(default='runs through November 3rd, 2013. There are 130 more performances and programs from local artists including Peter Glantz and Meredith Stern.')),
        ))
        db.send_create_signal(u'receipt', ['Show'])

        # Adding model 'Artist'
        db.create_table(u'receipt_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pseudonym', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('artist_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('twitterhandle', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'receipt', ['Artist'])

        # Adding model 'Event'
        db.create_table(u'receipt_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length='255', blank=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='', max_length='255', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'receipt', ['Event'])

        # Adding M2M table for field artist on 'Event'
        db.create_table(u'receipt_event_artist', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'receipt.event'], null=False)),
            ('artist', models.ForeignKey(orm[u'receipt.artist'], null=False))
        ))
        db.create_unique(u'receipt_event_artist', ['event_id', 'artist_id'])


    def backwards(self, orm):
        # Deleting model 'Show'
        db.delete_table(u'receipt_show')

        # Deleting model 'Artist'
        db.delete_table(u'receipt_artist')

        # Deleting model 'Event'
        db.delete_table(u'receipt_event')

        # Removing M2M table for field artist on 'Event'
        db.delete_table('receipt_event_artist')


    models = {
        u'receipt.artist': {
            'Meta': {'object_name': 'Artist'},
            'artist_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pseudonym': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitterhandle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'receipt.event': {
            'Meta': {'object_name': 'Event'},
            'artist': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['receipt.Artist']", 'symmetrical': 'False', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': "'255'", 'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': "'255'", 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'receipt.show': {
            'Meta': {'object_name': 'Show'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'default': "'runs through November 3rd, 2013. There are 130 more performances and programs from local artists including Peter Glantz and Meredith Stern.'"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Locally Made'", 'max_length': '255'})
        }
    }

    complete_apps = ['receipt']