# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from forms import *
from core.shortcuts import *
from core.decorators import *
from core.views import updateTimeout
from django.utils import simplejson

@login_required()
def overview(request):
    updateTimeout(request)
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact).filter(trashed=False)
    return render_with_request(request, 'contacts/list.html', {'title': _('Contacts'), 'contacts': contacts})

@login_required()
def overview_trashed(request):
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact).filter(trashed=True)
    return render_with_request(request, 'contacts/list.html', {'title': _('Deleted contacts'), 'contacts': contacts})

@login_required()
def overview_all(request):
    contacts = Core.current_user().getPermittedObjects("VIEW", Contact)
    return render_with_request(request, 'contacts/list.html',
                               {'title': _("All deleted contacts"), 'contacts': contacts})

@require_permission("CREATE", Contact)
def add(request):
    return form(request)

@require_permission("EDIT", Contact, "id")
def edit(request, id):
    return form(request, id)

@require_permission("VIEW", Contact, "id")
def view(request, id):
    contact = get_object_or_404(Contact, id=id)
    return render_with_request(request, 'contacts/view.html', {'title': _('Contact'), 'contact': contact})

@require_permission("DELETE", Contact, "id")
def delete(request, id):
    Contact.objects.get(id=id).delete()
    return redirect(overview)


@require_permission("CREATE", Contact)
def add_ajax(request):
    form = ContactForm(request.POST, instance=Contact())

    if form.is_valid():
        a = form.save()

        return HttpResponse(simplejson.dumps({'name': a.full_name,
                                              'id': a.id}), mimetype='application/json')

    print form.errors

    return HttpResponse("ERROR")

@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Contact, id=id, deleted=False)
        msg = _("Successfully edited contact")
    else:
        instance = Contact()
        msg = _("Successfully added new contact")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            request.message_success(msg)

            return redirect(edit, o.id)
    else:
        form = ContactForm(instance=instance)

    contacts = Core.current_user().getPermittedObjects("VIEW", Contact)

    return render_with_request(request, "contacts/form.html", {'title': _("Contact"),
                                                               'form': form,
                                                               'contacts': contacts,
                                                               })