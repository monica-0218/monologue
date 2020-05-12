from django.contrib import admin
from blog.models import Category, Tag, Post, ContentImage, Comment, Reply, New, Novel, Chapter, Story


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
    ]


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('novel', 'chapter_num', 'chapter_title')


class StoryAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'story_num', 'story_title')


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(New)
admin.site.register(Novel)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Story, StoryAdmin)
