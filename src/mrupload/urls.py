from django.conf.urls import url

from .views import UploadView, LibraryView, VideoUpdateView

urlpatterns = [
    url(regex=r'^$',
        view=LibraryView.as_view(),
        name='library'),
    url(regex=r'^upload/$',
        view=UploadView.as_view(),
        name='upload_videos'),
    url(regex=r'^update/(?P<pk>[0-9]+)/$',
        view=VideoUpdateView.as_view(),
        name='update_video'),
]
