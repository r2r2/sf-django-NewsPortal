from django.contrib import admin

from news.models import Author, Category, Post, Comment, UserCategorySub


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCategorySub)
class UserCategorySub(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('date_creation', )
    list_display = ('author', 'article_or_news', 'post_title', 'post_rating', 'date_creation')
    fieldsets = (
        (None, {
            'fields': ('author', 'article_or_news', 'post_title', 'post_text', 'post_rating')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
