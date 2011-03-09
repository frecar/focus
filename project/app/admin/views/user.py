# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import get_object_or_404, HttpResponse
from django.db.models import Q
from core.shortcuts import *
from core.views import updateTimeout
from core.decorators import *
from core.models import User, Permission
from app.admin.forms import *
from django.utils.translation import ugettext as _

@login_required()
def overview(request):
    updateTimeout(request)
    Users = User.objects.inCompany()
    return render_with_request(request, 'admin/users/list.html', {'title': _("Users"), 'users': Users})

@login_required()
def grant_permissions(request):
    Users = User.objects.all()
    Permissions = Permission.objects.all()
    return render_with_request(request, 'admin/users/grant_permssions.html',
                               {'title': _("Users"), 'users': Users, 'permissions': Permissions})

@login_required()
def add(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def editProfile(request):
    pass

@login_required()
def changeCanLogin(request, id):
    u = User.objects.get(id=id)

    if u == request.user:
        request.messages_error(_("You can't change your own login status"))
        return redirect(view, id)

    u.canLogin = not u.canLogin
    u.save()
    return redirect(view, id)

@login_required()
def sendGeneratedPassword(request, id):
    user = get_object_or_404(User, id=id, company=request.user.get_company())

    import string
    import random

    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [a for a in string.ascii_lowercase if a not in vowels]
    ret = ''
    slen = 8

    for i in range(slen):
        if i % 2 == 0:
            randid = random.randint(0, 20) #number of consonants
            ret += consonants[randid]
        else:
            randid = random.randint(0, 4) #number of vowels
            ret += vowels[randid]

    ret += "%s" % random.randint(20, 99)

    from django.core.mail import send_mail

    send_mail('Nytt passord', 'Nytt passord er: %s' % ret, 'FocusTime',
              ["%s" % user.email], fail_silently=False)

    user.set_password("%s" % ret)
    user.save()

    if settings.DEBUG:
        print "Nytt passord er: %s" % ret

    request.message_success(_("Successfully sent new password"))

    return redirect(view, id)

@login_required()
def addPop(request):
    instance = User()

    if request.method == "POST":
        form = UserForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()

            form.save_m2m()

            if not o.get_profile().company:
                o.get_profile().company = request.user.get_profile().company
                o.get_profile().save()
                sendGeneratedPassword(request, o.id)

            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    ((o._get_pk_val()), (o)))

    else:
        form = UserForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Bruker', 'form': form})


@login_required()
def view(request, id):
    user = User.objects.get(id=id)
    Permissions = user.get_permissions()

    return render_with_request(request, 'admin/users/view.html', {'title': _("User"),
                                                                  'userCard': user,
                                                                  'permissions': Permissions,
                                                                  })

@login_required()
def delete(request, id):
    u = User.objects.get(id=id)
    u.is_active = False
    u.save()
    request.message_success(_("Successfully deletes user"))
    return redirect(overview)


@login_required()
def setHourRegistrationLimitsManually (request, id):
    instance = get_object_or_404(User, id=id)
    msg = _("Successfully changed user")

    if request.method == 'POST':
        form = HourRegistrationManuallyForm(request.POST, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)

            o.save()
            form.save_m2m()

            request.message_success(msg)

            return redirect(view, id)

    else:
        form = HourRegistrationManuallyForm(instance=instance)

    return render_with_request(request, "admin/users/form.html", {'title': _("Change user"),
                                                                  'userCard':instance,
                                                                   'form': form})


@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(User, id=id, company=request.user.company)
        msg = _("Successfully edited user")
    else:
        instance = User()
        msg = _("Successfully added new user")

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = UserForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)

            new = False
            if not o.id:
                new = True

            o.save()
            form.save_m2m()

            if not o.get_company():
                o.set_company()

            if new:
                #send new generated password to the new user
                sendGeneratedPassword(request, o.id)

                #Add the new user to allemployee group of the company
                if Core.current_user().get_company_allemployeesgroup():
                    Core.current_user().get_company_allemployeesgroup().addMember(o)

            request.message_success(msg)

            #Redirects after save for direct editing
            return redirect(overview)

    else:
        form = UserForm(instance=instance)

    return render_with_request(request, "admin/users/form.html",
                               {'title': _("User"), 'userCard': instance, 'form': form})