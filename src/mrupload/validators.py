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
