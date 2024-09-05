from django.core.management.base import BaseCommand, CommandError
from news.models import 
class Command(BaseCommand):
	help = 'Обнуляет количество всех товаров'

	def handler(self, *args, **options):
		pass