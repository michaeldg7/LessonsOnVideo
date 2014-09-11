from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from lessons.models import VideoLesson


def homepage(request, template_name="index.html"):
    """
    Displays the home page
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
