import requests

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from embed_video.backends import detect_backend
from embed_video.fields import EmbedVideoField
from ordered_model.models import OrderedModel


class Category(models.Model):
    """
    Stores information about Video Categories.
    """
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return "%s" % (self.title, )

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = '%s' % (slugify(self.title), )
            self.save()


class VideoLesson(OrderedModel):
    """
    Stores information about Video Lessons
    """
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    video = EmbedVideoField()
    info = models.TextField(blank=True, null=True)
    order_with_respect_to = 'category'

    class Meta:
        verbose_name = "Video Lesson"
        verbose_name_plural = "Video Lessons"

    def _get_youtube_info(self, backend):
        info = ""
        try:
            req = requests.get("http://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=%s&format=json" % (backend.code))
            info = req.text
        except:
            pass
        return info

    def save(self, *args, **kwargs):
        super(VideoLesson, self).save(*args, **kwargs)

        if not self.info:
            backend = detect_backend(self.video)
            try:
                self.info = backend.info
            except:
                self.info = self._get_youtube_info(backend)
            self.save()
