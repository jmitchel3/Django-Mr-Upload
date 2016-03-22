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

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['file'] = forms.FileField(widget=forms.FileInput)

        if self.instance.pk:
            current_file_link = 'Currently: <a href="{file_url}">{file_name}</a>'
            self.fields['file'].help_text = current_file_link.format(
                file_url=self.instance.get_file_secure_url(),
                file_name=self.instance.file.name,
            )


class MultipleFileForm(FileFormMixin, forms.Form):
    video_files = MultipleUploadedFileField(label='Drop files to upload.')
