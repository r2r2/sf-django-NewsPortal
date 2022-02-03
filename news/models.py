from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from pytils.translit import slugify


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    author_rating = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)

    def update_rating(self):
        post_rate = self.post_set.aggregate(Sum('post_rating'))
        p_rat = 0
        p_rat += post_rate.get('post_rating__sum')

        comment_rate = self.author_name.comment_set.aggregate(comment_rating=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_rate.get('comment_rating')

        comment_post_rate = self.post_set.aggregate(comment_rating=Sum('comment__comment_rating'))
        cp_rat = 0
        cp_rat += comment_post_rate.get('comment_rating')

        self.author_rating = p_rat * 3 + c_rat + cp_rat
        self.save()

    def __str__(self):
        return f"{self.author_name}\n" \
               f"(rating:{self.author_rating})"

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True, verbose_name='Категория')
    subscribers = models.ManyToManyField(User, through='UserCategorySub')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"{self.category_name}"

    def get_absolute_url(self):
        return reverse('news:news')


class UserCategorySub(models.Model):
    """M2M table"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} = {self.category}"


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    CHOICE = [
        (ARTICLE, 'article'),
        (NEWS, 'news'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    article_or_news = models.CharField(max_length=10,
                                       choices=CHOICE,
                                       default=NEWS)
    date_creation = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    post_title = models.CharField(max_length=128, null=True, verbose_name='Заголовок')
    post_text = models.TextField(verbose_name='Текст статьи')
    post_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image = models.ImageField('Картинка', upload_to='news/%Y/%m/%d', null=True, blank=True)
    url = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    # Переопределяем save для кэширования и slug
    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.post_title)  # import slugify from pytils.translit для работы с кириллицей
        super(Post, self).save(*args, **kwargs)
        cache.delete(self.pk)

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.url})

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f"{self.post_text[:125]}..."

    def __str__(self):
        return f"{self.author}\n" \
               f"{self.post_rating}\n" \
               f"{self.post_title}\n" \
               f"{self.preview()}\n"


class PostCategory(models.Model):
    """M2M table"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    date_creation = models.DateTimeField(auto_now_add=True)
    comment_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f"{self.post}\n" \
               f"{self.user}\n" \
               f"{self.text}\n" \
               f"{self.date_creation}\n" \
               f"{self.comment_rating}"
