from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from news.models import News, Media, Comments


class NewsAdmin(ImportExportModelAdmin):
    search_fields = ['title', 'body']
    list_display = ['title', 'created', 'category']
    list_filter = ['created', 'updated', 'category']
    fields = ['title', 'image', 'category', 'body']


class MediaAdmin(ImportExportModelAdmin):
    pass


class CommentAdmin(ImportExportModelAdmin):
    pass


admin.site.register(News, NewsAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Comments, CommentAdmin)
