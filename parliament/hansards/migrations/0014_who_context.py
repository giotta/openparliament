# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Statement.source_id'
        db.add_column('hansards_statement', 'source_id', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True), keep_default=False)

        # Adding field 'Statement.who_context'
        db.add_column('hansards_statement', 'who_context', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Statement.source_id'
        db.delete_column('hansards_statement', 'source_id')

        # Deleting field 'Statement.who_context'
        db.delete_column('hansards_statement', 'who_context')


    models = {
        'bills.bill': {
            'Meta': {'ordering': "('privatemember', 'institution', 'number_only')", 'object_name': 'Bill'},
            'added': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'introduced': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'law': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'number_only': ('django.db.models.fields.SmallIntegerField', [], {}),
            'privatemember': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sessions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Session']", 'through': "orm['bills.BillInSession']", 'symmetrical': 'False'}),
            'short_title_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_title_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sponsor_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ElectedMember']", 'null': 'True', 'blank': 'True'}),
            'sponsor_politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Politician']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'status_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status_fr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'text_docid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'bills.billinsession': {
            'Meta': {'object_name': 'BillInSession'},
            'bill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bills.Bill']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduced': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'legisinfo_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Session']"}),
            'sponsor_member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ElectedMember']", 'null': 'True', 'blank': 'True'}),
            'sponsor_politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Politician']", 'null': 'True', 'blank': 'True'})
        },
        'core.electedmember': {
            'Meta': {'object_name': 'ElectedMember'},
            'end_date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Party']"}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Politician']"}),
            'riding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Riding']"}),
            'sessions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Session']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'})
        },
        'core.party': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'core.politician': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Politician'},
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'headshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_family': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name_given': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '30', 'blank': 'True'})
        },
        'core.riding': {
            'Meta': {'ordering': "('province', 'name')", 'object_name': 'Riding'},
            'edid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'})
        },
        'core.session': {
            'Meta': {'ordering': "('-start',)", 'object_name': 'Session'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parliamentnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sessnum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'hansards.document': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Document'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'document_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'most_frequent_word': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Session']"}),
            'source_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'wordcloud': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'hansards.statement': {
            'Meta': {'ordering': "('sequence',)", 'object_name': 'Statement'},
            'bills': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bills.Bill']", 'symmetrical': 'False', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {}),
            'content_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hansards.Document']"}),
            'h1': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'h2': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'h3': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ElectedMember']", 'null': 'True', 'blank': 'True'}),
            'mentioned_politicians': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'statements_with_mentions'", 'blank': 'True', 'to': "orm['core.Politician']"}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Politician']", 'null': 'True', 'blank': 'True'}),
            'procedural': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'statement_type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'who': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'who_context': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'who_hocid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wordcount': ('django.db.models.fields.IntegerField', [], {}),
            'written_question': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        }
    }

    complete_apps = ['hansards']
