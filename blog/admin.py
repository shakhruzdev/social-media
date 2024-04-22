from django.contrib import admin
from .models import Post, Comment, Like, Follow


class PostInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('id', 'author', 'post_image', 'is_published', 'view_count', 'created_at')
    list_display_links = ('id', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_visible', 'created_at')
    list_display_links = ('id', 'author')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    list_display_links = ('id', 'author')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('display_id', 'follower', 'following', 'created_at', 'updated_at')
    list_display_links = ('created_at',)

    def display_id(self, obj):
        return obj.id if obj.id is not None else "-"

    display_id.short_description = 'ID'
