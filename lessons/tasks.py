import requests
import urllib
import json

from django.conf import settings

from lessons.models import VideoLesson

from gdata.youtube import service

from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from haystack.management.commands import update_index

import logging
logger = logging.getLogger('django')


def create_lesson(creator, item, category, counter, remove_list):
    url = item.link[0].href.replace('&feature=youtube_gdata', '')
    try:
        lesson = VideoLesson()
        lesson.user = creator
        lesson.video = url
        lesson.title = item.media.title.text
        lesson.meta_title = item.media.title.text
        lesson.meta_description = item.media.description.text
        lesson.duration = item.media.duration.seconds
        lesson.category = category
        lesson.save(*{'entry': item})
        counter += 1
    except:
        remove_list.append(url)
        logger.info(">>>>> Could not create video in URL: {}".format(url))
    return counter, remove_list


@task
def create_videos_via_playlist(creator, playlist_url, category):
    """
    Task to create :model:'lessons.VideoLesson' objects using the parameters given
    """
    remove_list = []
    counter = 0

    yt_service = service.YouTubeService()
    yt_service.ssl = True
    yt_service.developer_key = settings.GOOGLE_DEVELOPER_KEY
    yt_service.client_id = settings.GOOGLE_CLIENT_ID

    logger.info(">>>>> Start creating videos")

    if '?v=' in playlist_url:
        item = yt_service.GetYouTubeVideoEntry(
            video_id=playlist_url.split('?v=')[1])
        counter, remove_list = create_lesson(
            creator, item, category, counter, remove_list)

    if '?list=' in playlist_url:
        full_url = "{}/playlists/{}".format(settings.YOUTUBE_URL_EXTRACTOR,
            url_type, playlist_url.split('?list=')[1])
        response = yt_service.GetYouTubePlaylistVideoFeed(uri=full_url)

        while response:
            for item in response.entry:
                counter, remove_list = create_lesson(
                    creator, item, category, counter, remove_list)
            response = yt_service.GetNext(response)

    VideoLesson.objects.filter(video__in=remove_list).delete()  # Hack to remove URLs that throws exception
    logger.info(">>>>> Successfully Created %s video/s." % (counter, ))
    update_index.Command().handle('lessons', remove=True)


@periodic_task(run_every=crontab(minute=0, hour='*/1'))
def update_lessons_index():
    logger.info("[Haystack] Updating lessons index...")
    update_index.Command().handle('lessons', remove=True)

