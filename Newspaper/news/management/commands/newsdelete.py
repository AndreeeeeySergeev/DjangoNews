from django.core.management.base import BaseCommand, CommandError
from news.models import Post

class Command(BaseCommand):
	help = 'удаляет все новости из категории'

	def add_arguments(self, parser):
		parser.add_argument('category', type='str')

	def handler(self, *args, **options):
		answer = input(f'Вы правда хотите удалить все категории {options["category"]}? yes/no')
		if answer != 'yes':
			self.stdout.write(self.style.ERROR('Отменено'))
			return
		try:
			category = Category.objects.get(name=options['category'])
			Post.objects.filter(category=category).delete()
			self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.name}'))
		except Category.DoesNotExist:
			self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))

		