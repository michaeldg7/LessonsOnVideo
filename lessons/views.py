from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from lessons.models import VideoLesson, Category


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
        paginator = Paginator(lessons_list, 6)
        lessons = paginator.page(page)
    except PageNotAnInteger:
        lessons = paginator.page(1)
    except EmptyPage:
        lessons = paginator.page(paginator.num_pages)

    context = {
        "lessons": lessons
    }
    return render_to_response(template_name, context, RequestContext(request))
