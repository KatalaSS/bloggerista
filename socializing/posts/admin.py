from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'modified']
    list_filter = ['created']
    prepopulated_fields = {"slug": ("title",)}
    view_on_site = True

admin.site.register(Post, PostAdmin)


