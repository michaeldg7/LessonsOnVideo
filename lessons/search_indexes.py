from haystack import indexes
from lessons.models import VideoLesson


class VideoLessonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    slug_auto = indexes.EdgeNgramField(model_attr='slug')
    description = indexes.CharField(model_attr='meta_description')
    thumbnail = indexes.CharField(model_attr='thumbnail')
    duration = indexes.IntegerField(model_attr='duration')

    def get_model(self):
        return VideoLesson

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
