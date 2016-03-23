import os

from django.core.files import File
from django.test import TestCase, override_settings
from django.test.client import Client
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import mock

from .models import Video


def get_temporary_video_file(file_name):
    current_path = os.path.dirname(os.path.realpath(__file__))
    file_path = 'test_files/test_quicktime_video.mov'
    full_path = os.path.join(current_path, file_path)
    f = open(full_path, 'r')
    temp_file = File(f)
    return temp_file


@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class LibraryViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.user = user
        self.client = Client()
        self.client.login(
            username=self.user.username,
            password='test',
        )
        Video.objects.create(
            user=self.user,
            file=get_temporary_video_file('TestVid'),
            title='test file',
            description='test desc',
        )
        self.url = reverse('library')

    def test_login_required_when_viewing_library(self):
        """
        User should be logged-in when viewing list of uploaded files.
        """
        # Given an un-authenticated user
        self.client.logout()

        # When the user goes to library page
        response = self.client.get(self.url)

        # User should be redirected to login page
        expected_url = '{}?next={}'.format(settings.LOGIN_URL, reverse('library'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    def test_list_videos_by_user(self):
        """
        A logged-in user should be able to see his videos.
        """
        # When the user goes to library page
        response = self.client.get(self.url)

        # User should see list of videos he uploaded
        expected_template = 'mrupload/library.html'
        expected_queryset = [repr(vid) for vid in Video.objects.filter(user=self.user)]
        self.assertTemplateUsed(response, expected_template)
        self.assertQuerysetEqual(response.context['video_list'], expected_queryset)


@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class UploadViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.user = user
        self.client = Client()
        self.client.login(
            username=self.user.username,
            password='test',
        )
        self.url = reverse('upload_videos')

    def test_login_required_when_uploading(self):
        """
        User should be logged-in when uploading videos.
        """
        # Given an un-authenticated user
        self.client.logout()

        # When the user goes to upload page
        response = self.client.get(self.url)

        # User should be redirected to login page
        expected_url = '{}?next={}'.format(settings.LOGIN_URL, reverse('upload_videos'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    def test_upload_page_for_logged_in_user(self):
        """
        A logged-in user should be able to access the upload page.
        """
        # When an authenticated user goes to upload page
        response = self.client.get(self.url)

        # User should land in the page with no problems!
        expected_template = 'mrupload/upload.html'

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template)

    def test_upload_succesful(self):
        """
        If uploading was successful, `Video` objects should be created
        and the user must be redirected to the library page.
        """
        # Assuming these files are the uploaded by the user through the form
        temp_video_files = [
            get_temporary_video_file('Video #1'),
        ]
        post_data = {
            'video_files': temp_video_files,
            'form_id': 'dummy-hash-id',
        }

        # When the form is submitted
        response = self.client.post(self.url, post_data)

        # Then the `Video` objects should be created
        self.assertEqual(len(temp_video_files), Video.objects.count())

        # Then the user should be redirected to the library page
        expected_url = reverse('library')
        self.assertRedirects(response, expected_url, status_code=302)


@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class VideoUpdateViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.user = user
        self.client = Client()
        self.client.login(
            username=self.user.username,
            password='test',
        )
        self.video = Video.objects.create(
            user=self.user,
            file=get_temporary_video_file('TestVid'),
            title='test file',
            description='test desc',
        )

    def test_login_required_when_updating_video(self):
        """
        User should be authenticated before updating a Video
        """
        # Given an un-authenticated user
        self.client.logout()

        # When user tries to update a video
        response = self.client.get(reverse('update_video', kwargs={'pk': self.video.pk}))

        # Then user should be redirected to the login page
        # User should be redirected to login page
        expected_url = '{}?next={}'.format(
            settings.LOGIN_URL,
            reverse('update_video', kwargs={'pk': self.video.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    @mock.patch.object(Video, 'get_file_secure_url')
    def test_update_page_for_authenticated_user(self, get_file_secure_url):
        """
        A logged-in user should be able to access the update video page.
        """
        # When user tries to update a video
        response = self.client.get(reverse('update_video', kwargs={'pk': self.video.pk}))

        # Then the user should land in the page with no problems!
        self.assertTemplateUsed(response, 'mrupload/update_video.html')

    def test_updating_a_video_not_owned_by_user(self):
        """
        Editing a Video not owned by the user should result to a 404 page
        """
        # When user tries to edit a video he doesn't own
        dummy_video_id = 999
        response = self.client.get(reverse('update_video', kwargs={'pk': dummy_video_id}))

        # Then the user should land on a 404 page
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(Video, 'get_file_secure_url')
    def test_update_video_details_succesful(self, get_file_secure_url):
        """
        When a user edits information on the `Video` object, he should
        be redirect to the library page.
        """
        post_data = {
            'title': 'New Title',
            'description': 'New Description',
        }
        response = self.client.post(
            reverse('update_video', kwargs={'pk': self.video.pk}),
            post_data,
        )

        updated_video = Video.objects.first()
        expected_url = reverse('library')
        self.assertEqual(updated_video.title, 'New Title')
        self.assertEqual(updated_video.description, 'New Description')
        self.assertRedirects(response, expected_url, status_code=302)
