from django.contrib import admin

# Register your models here.
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user', 'description', 'avatar']


admin.site.register(UserProfile, UserProfileAdmin)


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ['title', 'category', 'author', 'created_at', 'tag']


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['title']
    list_display = ['title', 'cover']


admin.site.register(Category, CategoryAdmin)
