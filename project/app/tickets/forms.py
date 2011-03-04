from django.forms.models import ModelForm
from app.tickets.models import Ticket, TicketUpdate
from core.models import User
from django import forms
from django.utils.translation import ugettext as _

ticket_fields = ('title', 'customer', 'description', 'status', 'priority', 'type', 'estimated_time', 'assigned_to', 'attachment',)

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'customer', 'description', 'status', 'priority', 'type', 'estimated_time', 'assigned_to', 'attachment',)

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.inCompany()
        self.fields['attachment'].required = False

class EditTicketForm(ModelForm):
    comment = forms.CharField(widget=forms.Textarea, label=_("Add Comment"))
    attachment = forms.FileField(label=_("Add Attachment"))
    class Meta:
        model = Ticket
        fields = ('title', 'customer', 'description', 'status', 'priority', 'type', 'estimated_time', 'assigned_to', 'spent_time',)

    def __init__(self, *args, **kwargs):
        super(EditTicketForm, self).__init__(*args, **kwargs)
        self.fields['attachment'].required = False

    def save(self, commit=True):
        ticket = super(EditTicketForm, self).save(commit)
        if commit:
            TicketUpdate.objects.create(ticket=ticket,
                                        comment=self.cleaned_data['comment'],
                                        attachment=self.cleaned_data['attachment'])
