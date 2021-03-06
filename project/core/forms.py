from core.utils import get_content_type_for_model
from core.models import Comment
from django.forms.models import ModelForm

class CommentForm(ModelForm):
    def __init__ (self, object, *args, **kwargs):
        object_id = object.id
        content_type = get_content_type_for_model(object)
        # If there is no instance, make a fake one!
        if not 'instance' in kwargs:
            kwargs['instance'] = Comment(object_id=object_id, content_type=content_type)

        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text',)