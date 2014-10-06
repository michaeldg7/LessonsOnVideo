from django.conf.urls import patterns, url

urlpatterns = patterns('lessons.views',
        # aJax Calls
        url(r'^category/ajax/(?P<category_slug>.*\w+)/$', 'category_videos_ajax',
            name="category_videos_ajax"),

        url(r'^video/(?P<video_slug>.*\w+)/$', 'video_detail', name="video_detail"),
        url(r'^category/(?P<category_slug>.*\w+)/$', 'category_videos', name="category_videos"),
        url(r'^videos/create/$', 'create_playlist_videos', name="create_playlist_videos"),
    )
