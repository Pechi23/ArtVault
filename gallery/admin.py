from django.contrib import admin

from .models import Gallery, Comment, Like, Follow, Image

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'views', 'created_at']
    search_fields = ['title', 'user']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'id', 'created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'gallery', 'created_at']
    search_fields = ['user', 'gallery']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'gallery', 'created_at']
    search_fields = ['user', 'gallery']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'followed', 'created_at']
    search_fields = ['user', 'followed']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    
