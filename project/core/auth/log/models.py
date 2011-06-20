# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from core import Core
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _

class Log(models.Model):
    date = models.DateTimeField()
    creator = models.ForeignKey("user.User", related_name="logs", null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    message = models.TextField()
    company = models.ForeignKey("company.Company", related_name="logs", null=True)
    action = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return "%s, %s:" % (self.date, self.content_type)

    def get_changes(self):
        msg = ""

        for k, v in eval(self.message).iteritems():
            msg += unicode(v[1]) + "endret til " + unicode(v[0])

        return msg

    def changed_since_last_time(self):
        #lastLog = self.get_object().getLogs().filter(id__lt=self.id)

        lastLog = Log.objects.filter(content_type=self.content_type, object_id=self.object_id).filter(id__lt=self.id)

        try:
            obj = self.content_type.get_object_for_this_type(id=self.object_id)
        except:
            return ""

        """
        Needs optimalization
        """

        diff = []

        fields = {}
        for a in obj._meta.fields:
            if 'related' in a.__dict__:
                fields[a.attname] = a.related.parent_model

        if lastLog:
            msg = ""
            lastLog = lastLog[len(lastLog) - 1]
            for i, value in eval(self.message).iteritems():
                if i == "id" or i == "date_created" or i == "date_edited":
                    continue

                if i not in eval(lastLog.message):
                    continue

                if i in fields:
                    if eval(self.message)[i][0] != eval(lastLog.message)[i][0]:
                        lastObj = fields[i].objects.get(id=eval(lastLog.message)[i][0])
                        newObj = fields[i].objects.get(id=eval(self.message)[i][0])

                        diff.append(value[1] + _(" was changed from %s to %s \n") % (
                        lastObj, newObj))
                    continue

                if eval(self.message)[i][0] != eval(lastLog.message)[i][0]:
                    diff.append(value[1] + _(" was changed from %s to: %s \n") % (
                    eval(lastLog.message)[i][0], eval(self.message)[i][0]))

            if len(diff) == 0:
                diff.append(_("No changes"))

            return diff

        diff.append(_("%s was created") % self.get_object())

        return diff

    def get_object(self, *args, **kwargs):
        try:
            o = ContentType.objects.get(model=self.content_type)
            k = o.get_object_for_this_type(id=self.object_id)
            return k
        except:
            return None
        
    def save(self, *args, **kwargs):
        self.date = datetime.now()

        if 'user' in kwargs:
            self.creator = kwargs['user']
        else:
            self.creator = Core.current_user()

        super(Log, self).save()


class Notification(models.Model):
    recipient = models.ForeignKey("user.User", related_name="notifications")
    text = models.TextField()
    read = models.BooleanField(default=False)
    log = models.ForeignKey(Log, null=True)

    #If true, add note to daily-mail updates
    sendEmail = models.BooleanField(default=False)

    def __unicode__(self):
        if self.log:
            return self.log.changed_since_last_time()
        return self.text

    def get_object(self, *args, **kwargs):
        if self.log:
            return self.log.get_object()
        return None