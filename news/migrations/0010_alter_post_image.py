# Generated by Django 4.0.2 on 2022-02-02 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news/%Y/%m/%d', verbose_name='Картинка'),
        ),
    ]