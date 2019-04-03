from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    help = 'Seeds the database'

    def handle(self, *args, **options):
        call_command('loaddata', 'products.json')
