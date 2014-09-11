from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from lessons.models import VideoLesson, Category


def homepage(request, template_name="index.html"):
    """
    Displays the home page

    **Context**

        ''lessons''
            A queryset of all 'lessons.VideoLesson' objects.

        ''RequestContext

    **Template:""

        :template:'index.html'

    """
    lessons = VideoLesson.objects.all()
    context = {
        "lessons": lessons,
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
    context = {
        "lesson": lesson
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
    lessons = VideoLesson.objects.filter(category=category)
    context = {
        "category": category,
        "lessons": lessons
    }
    return render_to_response(template_name, context, RequestContext(request))
