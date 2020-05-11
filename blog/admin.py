from django.contrib import admin

from blog.models import Category, Tag, Post, ContentImage, Comment, Reply, New, Novel, Chapter, Story


class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
    ]

class NovelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(New)
admin.site.register(Novel, NovelAdmin)
admin.site.register(Chapter)
admin.site.register(Story)
