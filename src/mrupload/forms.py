from django import forms

from .models import Video


class VideoModelForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            'file',
            'description',
        ]


