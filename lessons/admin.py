import ast

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

    list_display = ('get_title', 'order', 'move_up_down_links')
    ordering = ('order', )

    readonly_fields = ['get_title', ]
    fieldsets = (
        ('Owner', {
            'fields': ('user', )
        }),
        ('Video Info', {
            'fields': ('get_title', 'video', 'category')
        }),
        )

    def get_title(self, obj):
        title = "[No Title]"
        if obj and obj.info:
            try:
                info = ast.literal_eval(obj.info)
                title = info['title']
            except:
                pass
        return title
    get_title.short_description = "Title"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        if obj:
            readonly_fields += ['get_title']
        return readonly_fields

admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoLesson, VideoLessonAdmin)
