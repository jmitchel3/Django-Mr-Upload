from django.contrib.auth.decorators import login_required

from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, Http404 
from django.utils import timezone


# Create your views here.
from .models import Video
from .forms import VideoModelForm

@login_required
def formset_upload_view(request):
    VideoModelFormset = modelformset_factory(Video, form=VideoModelForm)
    formset = VideoModelFormset(request.POST or None, request.FILES or None)
    if formset.is_valid():
        #formset.save(commit=False)
        for form in formset:
            obj = form.save(commit=False)
            if form.cleaned_data:
                obj.user = request.user
                obj.save()
    context = {
        "formset": formset
    }
    return render(request, "mrupload/formset_upload_view.html", context)