import re
import requests
import urllib

from django.conf import settings

from lessons.models import VideoLesson

from celery import task

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
    req = requests.get(full_url, verify=False, timeout=600)
    response = req.text
    urls = re.split('[\xef\xbb\xbf\r\n]', response)
    urls = filter(None, urls)

    counter = 0
    logger.info(">>>>> Start creating %s videos" % (len(urls), ))
    for url in urls:
        try:
            VideoLesson.objects.create(
                user=creator,
                video=url,
                category=category
            )
            counter += 1
        except:
            error_msg = ">>>>> Could not create video in URL: %s" % (url, )
            logger.info(error_msg)

    logger.info(">>>>> Successfully Created %s video/s." % (counter, ))
