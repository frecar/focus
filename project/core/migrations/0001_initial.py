# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Company'
        db.create_table('core_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('adminGroup', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='companiesWhereAdmin', null=True, to=orm['core.Group'])),
            ('allEmployeesGroup', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='companiesWhereAllEmployeed', null=True, to=orm['core.Group'])),
            ('daysIntoNextMonthHourRegistration', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('hoursNeededFor50overtimePay', self.gf('django.db.models.fields.IntegerField')(default=160)),
            ('hoursNeededFor100overtimePay', self.gf('django.db.models.fields.IntegerField')(default=240)),
        ))
        db.send_create_signal('core', ['Company'])

        # Adding model 'User'
        db.create_table('core_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='core_user_users', null=True, to=orm['core.Company'])),
            ('canLogin', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('profileImage', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('validEditHourRegistrationsFromDate', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('validEditHourRegistrationsToDate', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('hourly_rate', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('percent_cover', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('core', ['User'])

        # Adding model 'Group'
        db.create_table('core_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['core.Group'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groups', null=True, to=orm['core.Company'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Group'])

        # Adding M2M table for field members on 'Group'
        db.create_table('core_group_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['core.group'], null=False)),
            ('user', models.ForeignKey(orm['core.user'], null=False))
        ))
        db.create_unique('core_group_members', ['group_id', 'user_id'])

        # Adding model 'Log'
        db.create_table('core_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', null=True, to=orm['core.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', null=True, to=orm['core.Company'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal('core', ['Log'])

        # Adding model 'Notification'
        db.create_table('core_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['core.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Log'], null=True)),
            ('sendEmail', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['Notification'])

        # Adding model 'Action'
        db.create_table('core_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('verb', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['Action'])

        # Adding model 'Role'
        db.create_table('core_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('core', ['Role'])

        # Adding M2M table for field actions on 'Role'
        db.create_table('core_role_actions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('role', models.ForeignKey(orm['core.role'], null=False)),
            ('action', models.ForeignKey(orm['core.action'], null=False))
        ))
        db.create_unique('core_role_actions', ['role_id', 'action_id'])

        # Adding model 'Permission'
        db.create_table('core_permission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.Group'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='permissions', null=True, to=orm['core.Role'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('negative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('to_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Permission'])

        # Adding M2M table for field actions on 'Permission'
        db.create_table('core_permission_actions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('permission', models.ForeignKey(orm['core.permission'], null=False)),
            ('action', models.ForeignKey(orm['core.action'], null=False))
        ))
        db.create_unique('core_permission_actions', ['permission_id', 'action_id'])

        # Adding model 'Comment'
        db.create_table('core_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trashed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 16, 5, 47, 42, 272506))),
            ('date_edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 3, 16, 5, 47, 42, 272538))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='comment_created', null=True, blank=True, to=orm['core.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='comment_edited', null=True, blank=True, to=orm['core.User'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='comment_edited', null=True, blank=True, to=orm['core.Company'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
        ))
        db.send_create_signal('core', ['Comment'])


    def backwards(self, orm):
        
        # Deleting model 'Company'
        db.delete_table('core_company')

        # Deleting model 'User'
        db.delete_table('core_user')

        # Deleting model 'Group'
        db.delete_table('core_group')

        # Removing M2M table for field members on 'Group'
        db.delete_table('core_group_members')

        # Deleting model 'Log'
        db.delete_table('core_log')

        # Deleting model 'Notification'
        db.delete_table('core_notification')

        # Deleting model 'Action'
        db.delete_table('core_action')

        # Deleting model 'Role'
        db.delete_table('core_role')

        # Removing M2M table for field actions on 'Role'
        db.delete_table('core_role_actions')

        # Deleting model 'Permission'
        db.delete_table('core_permission')

        # Removing M2M table for field actions on 'Permission'
        db.delete_table('core_permission_actions')

        # Deleting model 'Comment'
        db.delete_table('core_comment')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.action': {
            'Meta': {'object_name': 'Action'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'core.comment': {
            'Meta': {'ordering': "['date_created']", 'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_created'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 16, 5, 47, 42, 272506)'}),
            'date_edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 3, 16, 5, 47, 42, 272538)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'comment_edited'", 'null': 'True', 'blank': 'True', 'to': "orm['core.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.company': {
            'Meta': {'object_name': 'Company'},
            'adminGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAdmin'", 'null': 'True', 'to': "orm['core.Group']"}),
            'allEmployeesGroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'companiesWhereAllEmployeed'", 'null': 'True', 'to': "orm['core.Group']"}),
            'daysIntoNextMonthHourRegistration': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'hoursNeededFor100overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '240'}),
            'hoursNeededFor50overtimePay': ('django.db.models.fields.IntegerField', [], {'default': '160'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'core.group': {
            'Meta': {'object_name': 'Group'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groups'", 'null': 'True', 'to': "orm['core.Company']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['core.Group']"})
        },
        'core.log': {
            'Meta': {'object_name': 'Log'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'null': 'True', 'to': "orm['core.Company']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'null': 'True', 'to': "orm['core.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Log']", 'null': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['core.User']"}),
            'sendEmail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'core.permission': {
            'Meta': {'object_name': 'Permission'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Action']", 'symmetrical': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.Role']"}),
            'to_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'permissions'", 'null': 'True', 'to': "orm['core.User']"})
        },
        'core.role': {
            'Meta': {'object_name': 'Role'},
            'actions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'role'", 'symmetrical': 'False', 'to': "orm['core.Action']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'canLogin': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'core_user_users'", 'null': 'True', 'to': "orm['core.Company']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'percent_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'profileImage': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'validEditHourRegistrationsFromDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'validEditHourRegistrationsToDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['core']
