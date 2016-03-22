from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text

import boto

User =  settings.AUTH_USER_MODEL


def mr_upload_location(instance, filename):
    return "{user}/videos/{file}".format(
            user=instance.user.username,
            file=filename
            )


class Video(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=120)
    file = models.FileField(upload_to=mr_upload_location)
    description = models.TextField()


    def __unicode__(self):
        return smart_text(self.title)

    def get_file_secure_url(self):
        """
        Returns a secure URL for the `file` that was uploaded to S3
        """
        conn = boto.s3.connect_to_region(
            settings.S3DIRECT_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            is_secure=True
        )
        bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = bucket.get_key(self.file.name)

        if key:
            return key.generate_url(expires_in=settings.AWS_FILE_EXPIRE, method='GET')


@receiver(post_save, sender=Video, dispatch_uid='new_video')
def new_video_created(sender, instance, created, **kwargs):
    if created:
        print 'URL of new Video is: %s' % instance.file.url
