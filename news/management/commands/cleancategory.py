from django.core.management.base import BaseCommand, CommandError

from news.models import Post


class Command(BaseCommand):
    help = 'Удаляет все посты из выбранной категории'
    missing_args_message = 'Введите название категории'

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Do you really want to delete all posts? yes/no')
        answer = input()

        if answer == 'yes':
            for cat in options["category"]:

                try:
                    Post.objects.filter(category__category_name__icontains=cat).delete()
                except Post.DoesNotExist:
                    raise CommandError(f'В категории {cat} нет постов')

                self.stdout.write(self.style.SUCCESS(f'Все посты в категории {cat} удалены'))
                return
        self.stdout.write(self.style.ERROR('Access denied'))
