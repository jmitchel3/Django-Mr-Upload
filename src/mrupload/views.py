from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, ListView, UpdateView

from .models import Video
from .forms import MultipleFileForm, VideoForm


class LibraryView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'mrupload/library.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UploadView(LoginRequiredMixin, FormView):
    form_class = MultipleFileForm
    template_name = 'mrupload/upload.html'
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        for video in form.cleaned_data['video_files']:
            Video.objects.create(
                user=self.request.user,
                title=video.name,
                file=video,
            )
        form.delete_temporary_files()
        return HttpResponseRedirect(self.get_success_url())


class VideoUpdateView(LoginRequiredMixin, UpdateView):
    model = Video
    template_name = 'mrupload/update_video.html'
    success_url = reverse_lazy('library')
    form_class = VideoForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            user=self.request.user,
            pk=self.kwargs.get('pk'),
        )
