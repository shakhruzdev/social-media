from django.contrib import admin
from .models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'follower_count', 'created_at')
    list_display_links = ('id', 'user')
