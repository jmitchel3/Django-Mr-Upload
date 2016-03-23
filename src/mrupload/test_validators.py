import os

from django.core.files import File
from django.core.exceptions import ValidationError
from django.test import TestCase

from .validators import validate_file_type


class ValidateFileTypeTest(TestCase):
    def setUp(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))

    def test_for_valid_file_type(self):
        # Given a valid video file (quicktime)
        file_path = 'test_files/test_quicktime_video.mov'
        full_path = os.path.join(self.current_path, file_path)

        # When validating the file type, no validation error should occur
        try:
            f = open(full_path, 'r')
            temp_file = File(f)
            validate_file_type(temp_file)
        except ValidationError:
            self.fail('ValidationError raised unexpectedly!')

    def test_for_invalid_file_type(self):
        # Given a file that is not a valid video file
        file_path = 'test_files/test_non_video_file.txt'
        full_path = os.path.join(self.current_path, file_path)

        # When validating the file type, a validation error should be raised
        with self.assertRaises(ValidationError):
            f = open(full_path, 'r')
            temp_file = File(f)
            validate_file_type(temp_file)
