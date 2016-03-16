from django.conf.urls import url, include

from .views import formset_upload_view

urlpatterns = [
    url(r'^$', formset_upload_view, name='upload')
]
