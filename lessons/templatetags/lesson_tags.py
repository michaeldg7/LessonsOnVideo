from django import template

from lessons.models import Category, VideoLesson

register = template.Library()


@register.filter
def convert_to_time(seconds):
    """
    Converts the given 'seconds' variable into readable time
    """
    h = 0
    m, s = divmod(seconds, 60)
    if m > 60:
        h, m = divmod(m, 60)

    duration = "%02d:%02d" % (m, s)
    if h > 0:
        duration = "%d:%02d:%02d" % (h, m, s)
    return duration


@register.filter
def get_children_categories(category):
    """
    Gets the children of the given category parameter
    """
    categories = Category.objects.filter(parent=category)
    return categories


@register.filter
def get_videos_by_categories(categories):
    """
    Returns 'lessons.VideoLesson' queryset based on the given list of categories.
    """
    if isinstance(categories, Category):
        return VideoLesson.objects.filter(category=categories)
    return VideoLesson.objects.filter(category__in=categories)
