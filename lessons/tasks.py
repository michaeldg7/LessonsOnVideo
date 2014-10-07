import requests
import urllib

from django.conf import settings

from lessons.models import VideoLesson

from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from haystack.management.commands import update_index

import logging
logger = logging.getLogger('django')


@task
def create_videos_via_playlist(creator, playlist_url, category):
    """
    Task to create :model:'lessons.VideoLesson' objects using the parameters given
    """
    values = {
        "pid": playlist_url,
        "API": 1,
    }
    data = urllib.urlencode(values)
    full_url = "%s?%s" % (settings.YOUTUBE_URL_EXTRACTOR, data)
    req = requests.get(full_url, verify=False, timeout=300)

    counter = 0
    logger.info(">>>>> Start creating videos")
    remove_list = []
    for index, url in enumerate(req.iter_lines()):
        if index == 0:
            url = url.replace("\xef\xbb\xbf", "")
        try:
            lesson = VideoLesson()
            lesson.user = creator
            lesson.video = url
            lesson.category = category
            lesson.save()
            counter += 1
        except:
            error_msg = ">>>>> Could not create video in URL: %s" % (url, )
            remove_list.append(url)
            logger.info(error_msg)

    VideoLesson.objects.filter(video__in=remove_list).delete()  # Hack to remove URLs that throws exception
    logger.info(">>>>> Successfully Created %s video/s." % (counter, ))
    update_index.Command().handle('lessons', remove=True)


@periodic_task(run_every=crontab(minute=0, hour='*/1'))
def update_lessons_index():
    logger.info("[Haystack] Updating lessons index...")
    update_index.Command().handle('lessons', remove=True)
