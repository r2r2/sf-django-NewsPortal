from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .forms import PostAdminForm
from .models import Author, Category, Post, Comment, UserCategorySub, PostCategory, Rating, RatingStar


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_rating')


@admin.register(UserCategorySub)
class UserCategorySub(admin.ModelAdmin):
    """М2М таблица подписчиков на категории"""
    list_display = ('user', 'category')
    list_filter = ('user', 'category')
    search_fields = ('user', 'category')


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('parent',)


class CategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    readonly_fields = ('date_creation', 'get_image')
    list_display = ('post_title', 'post_text', 'author', 'get_image', 'post_rating', 'date_creation')
    list_display_links = ("post_title", 'author')
    list_filter = ('author', 'post_rating', 'date_creation')
    search_fields = ('post_title', 'category__category_name')
    save_on_top = True
    prepopulated_fields = {"url": ("post_title",)}
    form = PostAdminForm
    inlines = [CategoryInline, CommentInline]
    save_as = True
    fieldsets = (
        (None, {
            'fields': ('author', 'post_title', 'url', 'post_rating', 'date_creation')
        }),
        ('Текст статьи:', {
            'classes': ('collapse', ),
            'fields': ('post_text', )
        }),
        (None, {
            'fields': (('image', 'get_image'),)
        }),
    )

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100" height="auto"')

    get_image.short_description = 'Картинка'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'user', 'text', 'date_creation')
    search_fields = ('user', 'post')
    list_filter = ('user', 'date_creation')
    readonly_fields = ('email', )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "post", "ip")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(RatingStar)

admin.site.site_title = 'News Portal'
admin.site.site_header = 'News Portal'
