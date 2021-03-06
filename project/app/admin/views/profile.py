# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from app.admin.forms import UserProfileForm, UserProfileImageForm, UserProfilePasswordForm
from django.shortcuts import render
from core.auth.user.models import User
from core.decorators import require_permission, login_required

@login_required()
def edit(request):
    try:
        instance = request.user
        msg = _("Successfully changed your profile")

    except Exception, e:
        request.message_error(_("Unknown profile"))
        return redirect("/")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            o.use_user_language(request)
            request.message_success(msg)
            return redirect(edit)

    else:
        form = UserProfileForm(instance=instance, initial={"profileImage": None})

    return render(request, "admin/profile/form.html", {'title': _('Profile'), 'form': form, 'userCard': instance})


@login_required()
def change_profile_image(request):
    try:
        instance = request.user
        msg = _("Successfully changed profile image")
    except Exception, e:
        request.message_error(_("Unknown profile"))
        return redirect("/")

    if request.method == 'POST':
        form = UserProfileImageForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(msg)
            return redirect(change_profile_image)
    else:
        form = UserProfileImageForm(instance=instance, initial={"profileImage": None})

    return render(request, "admin/profile/formimage.html",
            {'title': _('Profile picture'), 'form': form, 'userCard': instance})


@login_required()
def change_password(request):
    instance = request.user
    if request.method == 'POST':
        form = UserProfilePasswordForm(request.POST, user=instance)

        if form.is_valid():
            u = request.user
            u.set_password(form.cleaned_data['new_password'])
            u.save()

            request.message_success(_("Successfully edited password"))

            return redirect(edit)

    else:
        form = UserProfilePasswordForm(user=request.user)

    return render(request, "admin/profile/formpassword.html",
            {"title": _("Change password"), 'form': form, 'userCard': instance})