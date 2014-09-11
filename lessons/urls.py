from django.conf.urls import patterns, url

urlpatterns = patterns('lessons.views',
        url(r'^video/(?P<video_slug>.*\w+)/$', 'video_detail', name="video_detail"),
        url(r'^category/(?P<category_slug>.*\w+)/$', 'category_videos', name="category_videos"),
    )
