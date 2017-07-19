from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'modified']
    list_filter = ['created']
    prepopulated_fields = {"slug": ("title",)}
    view_on_site = True

    inlines = [
        CommentInline
    ]

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content', 'user', 'created', 'modified']
    list_filter = ['created']


admin.site.register(Comment, CommentAdmin)
