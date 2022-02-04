from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .forms import PostAdminForm
from .models import Author, Category, Post, Comment, UserCategorySub


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_rating')


@admin.register(UserCategorySub)
class UserCategorySub(admin.ModelAdmin):
    """М2М таблица подписчиков на категории"""
    list_display = ('user', 'category')
    list_filter = ('user', 'category')
    search_fields = ('user', 'category')


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    readonly_fields = ('date_creation', )
    list_display = ('author', 'post_title', 'post_text', 'post_rating', 'date_creation')
    list_filter = ('author', 'post_rating', 'date_creation')
    search_fields = ('post_title', 'category__category_name')
    save_on_top = True
    prepopulated_fields = {"url": ("post_title",)}
    form = PostAdminForm
    fieldsets = (
        (None, {
            'fields': ('author', 'post_title', 'url', 'image', 'post_text', 'post_rating', 'date_creation')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date_creation')
    search_fields = ('user', 'post')
    list_filter = ('user', 'date_creation')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
