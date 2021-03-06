# Generated by Django 4.0 on 2021-12-26 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date',
            new_name='date_creation',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='article',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='date',
            new_name='date_creation',
        ),
        migrations.RemoveField(
            model_name='author',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_name',
        ),
        migrations.AddField(
            model_name='author',
            name='author_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='post',
            name='post_title',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='post',
            name='article_or_news',
            field=models.CharField(choices=[('AR', 'article'), ('NW', 'news')], default='NW', max_length=10),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
