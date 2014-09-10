from django.contrib import admin

from embed_video.admin import AdminVideoMixin
from mptt.admin import MPTTModelAdmin
from ordered_model.admin import OrderedModelAdmin

from lessons.models import Category, VideoLesson


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

    list_display = ('title', 'order', 'move_up_down_links')
    ordering = ('order', )

    fieldsets = (
        ('Owner', {
            'fields': ('user', )
        }),
        ('Video Info', {
            'fields': ('video', 'category')
        }),
        )


    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = list(self.readonly_fields)
    #     if obj:
    #         readonly_fields += ['title', 'thumbnail']
    #     return readonly_fields

admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoLesson, VideoLessonAdmin)
