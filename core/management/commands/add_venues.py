from django.core.management.base import BaseCommand
from core.models import Venue, Category


class Command(BaseCommand):
    help = 'Add test venues to the database'

    def handle(self, *args, **kwargs):
        categories = [
            'Restauracja',
            'Kawiarnia',
            'Bar',
            'Pizzeria',
            'Kebab'
        ]

        # Create categories
        category_objects = []
        for category in categories:
            cat_obj, created = Category.objects.get_or_create(name=category)
            category_objects.append(cat_obj)

        # Create venues with URLs
        venues = [
            ('Nano Kebab Malczyńscy',
             'Bracia Malczyńscy to popularni polscy youtuberzy, a także zawodnicy Fame MMA, otworzyli kebab',
             category_objects[4], 'https://www.youtube.com/watch?v=1mnZ1tIBPXA'),
            ('Telepizza', 'Telepizza: opinie są podzielone, dostępna w całym kraju, sieć założona 1987',
             category_objects[3], 'https://www.youtube.com/watch?v=ATWBpHq4AlU'),
            ('Stołówka sejmu', 'Stołówka w sejmie RP', category_objects[2],
             'https://www.youtube.com/watch?v=ZdrWLjuaDp0'),
            ('U Fukiera', 'Restauracja Magdy Gessler', category_objects[0],
             'https://www.youtube.com/watch?v=iVG3kXZ51eI')
        ]

        for name, description, category, video_url in venues:
            Venue.objects.create(name=name, description=description, category=category, video_url=video_url)

        self.stdout.write(self.style.SUCCESS('Successfully added test venues.'))
