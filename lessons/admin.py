from django import forms
from django.contrib import admin

from embed_video.admin import AdminVideoMixin
from mptt.admin import MPTTModelAdmin
from ordered_model.admin import OrderedModelAdmin

from lessons.models import Category, VideoLesson, Product, ProductFile


class VideoLessonAdminForm(forms.ModelForm):
    class Meta:
        model = VideoLesson

    def __init__(self, *args, **kwds):
        super(VideoLessonAdminForm, self).__init__(*args, **kwds)

        related_videos = VideoLesson.objects.all()
        if self.instance:
            related_videos = related_videos.exclude(id=self.instance.id)
        self.fields['related_videos'].queryset = related_videos


class CategoryAdmin(MPTTModelAdmin):
    """
    Admin view for :model:'lessons.Category' model
    """
    model = Category
    prepopulated_fields = {"slug": ("title", )}
    mptt_level_indent = 20


class VideoLessonAdmin(AdminVideoMixin, OrderedModelAdmin):
    """
    Admin view for :model:'lessons.VideoLesson' model
    """
    model = VideoLesson
    form = VideoLessonAdminForm

    list_display = ('title', 'order', 'move_up_down_links')
    ordering = ('order', )
    filter_horizontal = ('related_videos', )

    fieldsets = (
        ('Owner', {
            'fields': ('user', )
        }),
        ('Video Info', {
            'fields': ('video', 'category')
        }),
        ('Related Videos', {
            'fields': ('related_videos', )
        }),
        ('Meta Data', {
            'fields': ('meta_title', 'meta_description', 'keywords')
        }),
        )


    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = list(self.readonly_fields)
    #     if obj:
    #         readonly_fields += ['title', 'thumbnail']
    #     return readonly_fields


class ProductFileInline(admin.StackedInline):
    """
    Inline view of ProductFile admin
    """
    model = ProductFile


class ProductAdmin(admin.ModelAdmin):
    """
    Admin view for :model:'lessons.Product' model
    """
    model = Product
    prepopulated_fields = {"slug": ("title", )}
    inlines = [ProductFileInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoLesson, VideoLessonAdmin)
# admin.site.register(Product, ProductAdmin)
