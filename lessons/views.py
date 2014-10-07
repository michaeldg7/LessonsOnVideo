from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from lessons.forms import PlaylistForm
from lessons.models import VideoLesson, Category
from lessons.social_apis import get_shares
from lessons.tasks import create_videos_via_playlist

import logging
logger = logging.getLogger('django')


def homepage(request, template_name="index.html"):
    """
    Displays the home page

    **Context**

        ''main_categories''
            A queryset of all 'lessons.Category' objects having no parent.

        ''RequestContext

    **Template:""

        :template:'index.html'

    """
    main_categories = Category.objects.filter(parent__isnull=True)
    context = {
        "main_categories": main_categories
    }
    return render_to_response(template_name, context, RequestContext(request))


def video_detail(request, video_slug, template_name="lessons/video.html"):
    """
    Displays 'lessons.VideoLesson' video as well as some of the details.
    This page also displays related videos as well as related products.

    **Context**

        ''lesson''
            An instance of 'lessons.VideoLesson'

        ''RequestContext

    **Template:""

        :template:'lessons/video.html'

    """
    lesson = get_object_or_404(VideoLesson, slug=video_slug)
    url = settings.SITE_FULL_DOMAIN + reverse("video_detail", args=(lesson.slug, ))
    shares = get_shares(url)
    context = {
        "lesson": lesson,
        "shares": shares,
        "APP_ID": settings.SOCIAL_AUTH_FACEBOOK_KEY,
        "SITE_TITLE": settings.SITE_TITLE
    }
    return render_to_response(template_name, context, RequestContext(request))


def category_videos(request, category_slug, template_name="lessons/category_videos.html"):
    """
    Displays 'lessons.VideoLesson' videos based on the given 'category_slug' parameter.
    This page will also display products based on the given category.

    **Context**

        ''category''
            An instance of 'lessons.Category'

        ''lessons''
            A queryset of 'lessons.VideoLesson' objects.

        ''RequestContext

    **Template:""

        :template:'lessons/category_videos.html'

    """
    category = get_object_or_404(Category, slug=category_slug)
    context = {
        "category": category
    }
    return render_to_response(template_name, context, RequestContext(request))


def category_videos_ajax(request, category_slug, template_name="lessons/ajax/category_videos_ajax.html"):
    """
    Displays 'lessons.VideoLesson' videos based on the given 'category_slug' parameter through aJax.

    **Context**

        ''lessons''
            A queryset of 'lessons.VideoLesson' objects.

        ''RequestContext

    **Template:""

        :template:'lessons/ajax/category_videos_ajax.html'

    """
    category = get_object_or_404(Category, slug=category_slug)
    lessons_list = VideoLesson.objects.filter(category=category)

    page = request.GET.get('page')
    try:
        paginator = Paginator(lessons_list, 9)
        lessons = paginator.page(page)
    except PageNotAnInteger:
        lessons = paginator.page(1)
    except EmptyPage:
        lessons = paginator.page(paginator.num_pages)

    context = {
        "lessons": lessons
    }
    return render_to_response(template_name, context, RequestContext(request))


@staff_member_required
def create_playlist_videos(request, template_name="lessons/create_playlist_videos.html"):
    """
    Displays form to create :model:'lessons.VideoLesson' objects.

    **Context**

        ''form''
            A PlaylistForm instance.

        ''RequestContext

    **Template:""

        :template:'lessons/create_playlist_videos.html'

    """
    form = PlaylistForm()
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_url = form.cleaned_data.get("url")
            category = form.cleaned_data.get("category")

            create_videos_via_playlist.delay(request.user, playlist_url, category)
            messages.success(request, "The videos will be available in a couple of minutes.")
            return HttpResponseRedirect(reverse('create_playlist_videos'))

    context = {
        "form": form
    }
    return render_to_response(template_name, context, RequestContext(request))
