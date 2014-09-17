import os
import decimal
import requests
import gdata.youtube
import gdata.youtube.service

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from embed_video.backends import detect_backend
from embed_video.fields import EmbedVideoField
from mptt.models import MPTTModel, TreeForeignKey
from ordered_model.models import OrderedModel


LEVEL_BEGINNER = 1
LEVEL_INTERMEDIATE = 2
LEVEL_ADVANCED = 3
PRODUCT_LEVEL_CHOICES = [
    (LEVEL_BEGINNER, "Beginner"),
    (LEVEL_INTERMEDIATE, "Intermediate"),
    (LEVEL_ADVANCED, "Advanced")
]


def get_image_path(instance, filename):
    """
    Dynamically set upload_to attribute of image fields.
    """
    classname = instance.__class__.__name__.lower()
    return os.path.join('shop', classname, filename)


def get_file_path(instance, filename):
    """
    Dynamically set upload_to attribute of file fields.
    """
    classname = instance.__class__.__name__.lower()
    return os.path.join('files', classname, filename)


class Category(MPTTModel):
    """
    Stores information about Video Categories.
    """
    parent = TreeForeignKey("self", blank=True, null=True, related_name='children')
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


class Product(models.Model):
    """
    Stores information about Product which will then be used in cartridge
    """
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = TreeForeignKey(Category)
    image = models.ImageField(upload_to=get_image_path)
    price = models.DecimalField(decimal_places=2, max_digits=7, default=decimal.Decimal('0.00'))
    admin_percentage = models.DecimalField(decimal_places=2, max_digits=7,
        help_text="Percentage of the Price that goes to Admin", default=decimal.Decimal('0.00'))
    author = models.ForeignKey(User)
    description = models.TextField()
    level = models.PositiveIntegerField(choices=PRODUCT_LEVEL_CHOICES, default=LEVEL_BEGINNER)
    approved = models.BooleanField(default=False)
    approved_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(default=datetime.now())
    # TODO: Add excess/bonus items

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __unicode__(self):
        return "%s" % (self.title, )

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(self.title)
            self.save()


class ProductFile(models.Model):
    """
    Stores Files related to Products
    """
    product = models.ForeignKey(Product)
    file_item = models.FileField(upload_to=get_file_path)

    class Meta:
        verbose_name = "Product File"
        verbose_name_plural = "Product Files"

    def __unicode__(self):
        return "%s" % (self.product.title, )


class VideoLesson(OrderedModel):
    """
    Stores information about Video Lessons
    """
    user = models.ForeignKey(User)
    category = TreeForeignKey(Category)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    duration = models.PositiveIntegerField("Duration in Seconds", default=0)
    video = EmbedVideoField()
    thumbnail = models.URLField(blank=True, null=True)
    backend_source = models.CharField(max_length=64, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    related_videos = models.ManyToManyField("self", blank=True, null=True)
    related_products = models.ManyToManyField(Product, blank=True, null=True)
    uploaded_date = models.DateTimeField(default=datetime.now())

    order_with_respect_to = 'category'

    class Meta:
        verbose_name = "Video Lesson"
        verbose_name_plural = "Video Lessons"

    # def _get_youtube_info(self, backend):
    #     info = ""
    #     try:
    #         req = requests.get("http://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=%s&format=json" % (backend.code))
    #         info = req.text
    #     except:
    #         pass
    #     return info

    def __unicode__(self):
        return "%s" % (self.title, )

    def _generate_youtube_info(self, entry):
        author = entry.author[0].name.text if entry.author and entry.author[0] else ""
        info = {
            "title": entry.media.title.text,
            "published_date": entry.published.text,
            "description": entry.media.description.text,
            "view_count": entry.statistics.view_count,
            "duration": entry.media.duration.seconds,
            "author": author
        }
        return info

    def _get_youtube_info(self, backend):
        yt_service = gdata.youtube.service.YouTubeService()
        yt_service.ssl = True
        yt_service.developer_key = settings.GOOGLE_DEVELOPER_KEY
        yt_service.client_id = settings.GOOGLE_CLIENT_ID

        entry = yt_service.GetYouTubeVideoEntry(video_id=backend.code)
        info = self._generate_youtube_info(entry)

        return info

    def save(self, *args, **kwargs):
        super(VideoLesson, self).save(*args, **kwargs)

        if not self.info:
            backend = detect_backend(self.video)

            if backend.backend == "VimeoBackend":
                info = backend.info
            elif backend.backend == "YoutubeBackend":
               info = self._get_youtube_info(backend)
               info.update({"id": backend.code})

            info.update({"backend": backend.backend})
            info.update({"thumbnail": backend.thumbnail})
            self.info = info
            self.title = info['title']
            self.slug = "%s-%s" % (self.id, slugify(self.title))
            self.duration = info['duration']
            self.backend_source = backend.backend
            self.thumbnail = backend.thumbnail
            self.save()