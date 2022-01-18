# Generated by Django 4.0.1 on 2022-01-15 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_rename_date_comment_date_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_title',
            field=models.CharField(max_length=128, null=True, verbose_name='Заголовок'),
        ),
    ]
