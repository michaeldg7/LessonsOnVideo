from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from embed_video.admin import AdminVideoMixin
from mptt.admin import MPTTModelAdmin
from ordered_model.admin import OrderedModelAdmin

from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost

from lessons.models import (HomePage, Category, VideoLesson,
    Product, ProductFile, Advertisement, BlogAdvertisement,
    HomePageVideo)


class HomePageAdmin(admin.ModelAdmin):
    fields = ('ad_top', 'ad_bottom_left', 'ad_bottom_right')

    def get_actions(self, request):
        return []

    def change_redirect(self):
        opts = HomePage._meta
        url = "admin:{}_{}_{}".format(
            opts.app_label, opts.object_name.lower(), "change")
        return HttpResponseRedirect(reverse(url, args=(1,)))

    def add_view(self, *args, **kwargs):
        return self.change_redirect()

    def changelist_view(self, *args, **kwargs):
        return self.change_redirect()

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class VideoLessonAdminForm(forms.ModelForm):
    class Meta:
        model = VideoLesson

    def __init__(self, *args, **kwds):
        super(VideoLessonAdminForm, self).__init__(*args, **kwds)

        related_videos = VideoLesson.objects.all()
        if self.instance:
            related_videos = related_videos.exclude(id=self.instance.id)
        self.fields['related_videos'].queryset = related_videos


class AdvertisementInline(admin.StackedInline):
    """
    Inline view of Advertisement admin
    """
    model = Advertisement
    extra = 4


class HomePageVideoInline(admin.StackedInline):
    """
    Inline view of HomePageVideo admin
    """
    model = HomePageVideo
    extra = 3


class CategoryAdmin(MPTTModelAdmin):
    """
    Admin view for :model:'lessons.Category' model
    """
    model = Category
    prepopulated_fields = {"slug": ("title", )}
    mptt_level_indent = 20
    inlines = [AdvertisementInline, HomePageVideoInline]

    fieldsets = (
        ('Info', {
            'fields': ('title', 'slug', 'parent', 'ad_top')
        }),
        ('Meta Data', {
            'fields': ('meta_title', 'meta_description', 'keywords')
        }),
        )


class VideoLessonAdmin(AdminVideoMixin, OrderedModelAdmin):
    """
    Admin view for :model:'lessons.VideoLesson' model
    """
    model = VideoLesson
    form = VideoLessonAdminForm

    list_display = ('title', 'category', 'order', 'move_up_down_links')
    ordering = ('order', )
    filter_horizontal = ('related_videos', )
    list_filter = ('category__title',)

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


class BlogAdvertisementInline(admin.StackedInline):
    """
    Inline view of Advertisement admin
    """
    model = BlogAdvertisement
    extra = 4

class MyBlogPostAdmin(BlogPostAdmin):
    inlines = [BlogAdvertisementInline]

admin.site.register(HomePage, HomePageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoLesson, VideoLessonAdmin)
# admin.site.register(Product, ProductAdmin)

admin.site.unregister(BlogPost)
admin.site.register(BlogPost, MyBlogPostAdmin)