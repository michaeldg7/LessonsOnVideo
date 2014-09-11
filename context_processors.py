from lessons.models import Category


def get_categories(request):
    config = {
        'CATEGORIES': Category.objects.all(),
    }
    return config
