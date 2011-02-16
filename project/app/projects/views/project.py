# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from app.contacts.models import Contact
from app.projects.forms import *
from core.models import Log
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

@require_permission("LIST", Project)
def overview(request):
    updateTimeout(request)
    projects = Core.current_user().getPermittedObjects("VIEW", Project).filter(trashed=False)
    return render_with_request(request, 'projects/list.html', {'title': 'Prosjekter', 'projects': projects})

@require_permission("LIST", Project)
def timeline(request):
    updateTimeout(request)
    #projects = Core.current_user().getPermittedObjects("VIEW", Project).filter(trashed=True)
    projects = Project.objects.all()
    return render_with_request(request, 'projects/timeline.html',
                               {'title': 'Tidslinje for alle prosjekter', 'projects': projects})

@require_permission("LIST", Project)
def overview_trashed(request):
    projects = Core.current_user().getPermittedObjects("VIEW", Project)
    return render_with_request(request, 'projects/list.html', {'title': 'Slettede prosjekter', 'projects': projects})

@require_permission("LIST", Project)
def overview_all(request):
    projects = Project.objects.all()
    return render_with_request(request, 'projects/list.html', {'title': 'Alle prosjekter', 'projects': projects})

@require_permission("VIEW", Project, 'id')
def view(request, id):
    project = Project.objects.get(id=id)
    whoCanSeeThis = project.whoHasPermissionTo('view')
    return render_with_request(request, 'projects/view.html', {'title': 'Prosjekt: %s' % project,
                                                               'project': project,
                                                               'whoCanSeeThis': whoCanSeeThis,
                                                               })

@require_permission("EDIT", Contact, "id")
def history(request, id):
    instance = get_object_or_404(Project, id=id, deleted=False)

    history = Log.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                 object_id=instance.id)

    return render_with_request(request, 'projects/log.html', {'title': _("Latest events"),
                                                              'project': instance,
                                                              'logs': history[::-1][0:150]})

@require_permission("CREATE", Project)
def add_ajax(request):
    form = ProjectFormSimple(request.POST, instance=Project())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.project_name,
                                              'id': a.id}), mimetype='application/json')
    
    return HttpResponse("ERROR")

@require_permission("CREATE", Project)
def add(request):
    return form(request)

@require_permission("EDIT", Project, 'id')
def edit(request, id):
    return form(request, id)

@require_permission("DELETE", Project, 'id')
def delete(request, id):
    project = Project.objects.get(id=id)
    if project.canBeDeleted()[0]:
        project.delete()
        request.message_success("Successfully deleted")
        return redirect(overview)
    else:
        request.message_error("You cannot delete this project: %s" % project.canBeDeleted()[1])
        return redirect(view, id)

def form (request, id=False):
    if id:
        instance = get_object_or_404(Project, id=id, deleted=False)
        title = _("Edit project")
        msg = "Vellykket endret prosjekt"
    else:
        instance = Project()
        msg = "Vellykket lagt til nytt prosjekt"
        title = _("New project")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            request.message_success(msg)

            return redirect(edit, o.id)

    else:
        form = ProjectForm(instance=instance)

    return render_with_request(request, "projects/form.html", {'title': title, 'project': instance, 'form': form})