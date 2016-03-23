from django.conf import settings
from django.core.exceptions import ValidationError

import magic


def validate_file_type(uf):
    """
    Raises a `ValidationError` if the mime type of the file
    is not under settings.VALID_FILE_MIME_TYPES
    """
    mime = magic.Magic(mime=True)
    mime_type = None

    for chunk in uf.chunks():
        mime_type = mime.from_buffer(chunk)
        break

    if mime_type not in settings.VALID_FILE_MIME_TYPES:
        error_msg = 'Invalid video file type.'
        raise ValidationError(error_msg)


def validate_file_size(uploaded_file):
    """
    Raises a `ValidationError` if the size of the uplaoded file is greater
    than `settings.MAX_VIDEO_FILE_SIZE`
    """
    file_size_in_kb = uploaded_file.size

    if file_size_in_kb > settings.MAX_VIDEO_FILE_SIZE:
        error_msg = 'Invalid file size. Maximum file size is %s MB.' % (
            settings.MAX_VIDEO_FILE_SIZE / 1000000,
        )
        raise ValidationError(error_msg)
