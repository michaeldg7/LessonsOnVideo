from django.shortcuts import render_to_response
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
