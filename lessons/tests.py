from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from django_webtest import WebTest
from django_dynamic_fixture import G

from gdata.youtube import service

from lessons.models import VideoLesson, Category


class LessonsTest(WebTest):
    fixtures = ['{}/category.json'.format(settings.FIXTURE_DIR)]
    user_name = 'test_user'
    email = 'test_user@example.com'
    password = 'password'
    test_playlist_url = 'https://www.youtube.com/playlist?list=PLy_9l13es1EtxLTI_OJBvMZFku14ywsk2'

    def setUp(self):
        super(LessonsTest, self).setUp()
        self.test_user = G(User, username=self.user_name, email=self.email,
                           is_staff=True)
        self.test_user.set_password(self.password)
        self.test_user.save()
        self.category = Category.objects.filter(parent__isnull=False).first()

    def test_create_playlist(self):

        yt_service = service.YouTubeService()
        yt_service.ssl = True
        yt_service.developer_key = settings.GOOGLE_DEVELOPER_KEY
        yt_service.client_id = settings.GOOGLE_CLIENT_ID
        full_url = "{}/playlists/{}".format(settings.YOUTUBE_URL_EXTRACTOR,
            self.test_playlist_url.split('?list=')[1])
        yt_response = yt_service.GetYouTubePlaylistVideoFeed(uri=full_url)

        count = int(yt_response.total_results.text)

        response = self.app.get(reverse('create_playlist_videos'),
                                user=self.user_name, status=200)
        form = response.forms["playlist-videos-form"]
        form['url'] = self.test_playlist_url
        form['category'] = self.category.id

        response = form.submit()

        self.assertRedirects(response, reverse('create_playlist_videos'))
        self.assertEqual(count, VideoLesson.objects.all().count())
