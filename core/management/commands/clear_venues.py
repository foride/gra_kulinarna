from django.core.management.base import BaseCommand
from core.models import Venue


class Command(BaseCommand):
    help = 'Delete all records from the Venue model'

    def handle(self, *args, **kwargs):
        Venue.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all Venue records.'))
