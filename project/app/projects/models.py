# -*- coding: utf-8 -*-
from django.db import models
from core import Core
from django.contrib.contenttypes import generic
from core.models import PersistentModel, User, Comment
from app.customers.models import Customer
from django.core import urlresolvers
from datetime import timedelta, datetime
import time
from django.utils.translation import ugettext as _

class Project(PersistentModel):
    pid = models.IntegerField(_("Project nuber"), null=True)
    POnumber = models.CharField(_("PO-number"), max_length=150, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), related_name="projects", default=None, null=True)
    project_name = models.CharField(_("Name"), max_length=80)
    description = models.TextField()
    deliveryAddress = models.CharField(max_length=150, null=True)
    responsible = models.ForeignKey(User, related_name="projectsWhereResponsible", verbose_name=_("Responsible"), null=True)
    deliveryDate = models.DateTimeField(verbose_name=_("Delivery date"), null=True, blank=True)
    deliveryDateDeadline = models.DateTimeField(verbose_name=_("Delivery deadline"), null=True, blank=True)
    comments = generic.GenericRelation(Comment)

    def __unicode__(self):
        return self.project_name

    def canBeDeleted(self):
        canBeDeleted = True
        reasons = []

        if self.orders.all().count() > 0:
            canBeDeleted = False
            reasons.append(_("Project has active orders"))

        if canBeDeleted:
            return (True, "OK")

        return (False, reasons)
    
    def getViewUrl(self):
        return urlresolvers.reverse('app.projects.views.view', args=("%s" % self.id,))

    def percentDone(self):
        if self.date_created and self.deliveryDate:
            realDiff = (time.mktime(datetime.now().timetuple()) - time.mktime(self.date_created.timetuple()))
            estimatedDiff = (time.mktime(self.deliveryDate.timetuple()) - time.mktime(self.date_created.timetuple()))

            if realDiff > estimatedDiff:
                return 100
            
            return (realDiff / estimatedDiff) * 100
        
        return 0

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.projects.views.project.add_ajax')

    @staticmethod
    def simpleform():
        return ProjectFormSimple(instance=Project(), prefix="projects")

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Project, self).save()

        #Give the user who created this ALL permissions on object
        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

class Milestone(PersistentModel):
    project = models.ForeignKey(Project, related_name="milestones")
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __unicode__(self):
        return "Milestone %s for project %s" % (self.name, self.project)

class ProjectFolder(PersistentModel):
    project_id = models.ForeignKey(Project, related_name="folders")
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "Prosjektmappe: %s" % self.name


class ProjectFile(PersistentModel):
    project_id = models.ForeignKey(Project, related_name="files")
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(ProjectFolder, related_name="files")

    def __unicode__(self):
        return "Prosjektfil: %s" % self.name


from app.projects.forms import ProjectFormSimple
