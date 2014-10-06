from django import forms

from mptt.forms import TreeNodeChoiceField

from lessons.models import Category


class PlaylistForm(forms.Form):
    """
    Form for extracting Youtube videos from the given Playlist URL
    """
    url = forms.URLField(max_length=255)
    category = TreeNodeChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super(PlaylistForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = "form-control"
