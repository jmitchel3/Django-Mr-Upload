from django import forms

from django_file_form.forms import FileFormMixin, MultipleUploadedFileField

from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            'file',
            'description',
        ]


class MultipleFileForm(FileFormMixin, forms.Form):
    video_files = MultipleUploadedFileField(label='Drop files to upload.')
