from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text

User =  settings.AUTH_USER_MODEL


def mr_upload_location(instance, filename):
    return "{user}/videos/{file}".format(
            user=instance.user.username,
            file=filename
            )


class Video(models.Model):
    user            = models.ForeignKey(User)
    title           = models.CharField(max_length=120)
    file            = models.FileField(upload_to=mr_upload_location)
    description     = models.TextField()


    def __unicode__(self):
        return smart_text(self.title)


@receiver(post_save, sender=Video, dispatch_uid='new_video')
def new_video_created(sender, instance, created, **kwargs):
    if created:
        print 'URL of new Video is: %s' % instance.file.url
