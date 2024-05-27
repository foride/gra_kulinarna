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

        # Create venues with additional fields
        venues = [
            ('Nano Kebab Malczyńscy', 'Bracia Malczyńscy to popularni polscy youtuberzy, a także zawodnicy Fame MMA, otworzyli kebab', category_objects[4], 'https://www.youtube.com/watch?v=1mnZ1tIBPXA', '1234', '13:00-22:00 Poniedziałek - Niedziela', 'Nowowiejska 82, 50-339 Wrocław', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2504.397729837239!2d17.05487347751666!3d51.11957133896002!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x470fe94ec435656d%3A0xe739b6fc359a5473!2sNano%20Kebab%20Malczy%C5%84scy!5e0!3m2!1spl!2spl!4v1716833681086!5m2!1spl!2spl'),
            ('Telepizza', 'Telepizza: opinie są podzielone, dostępna w całym kraju, sieć założona 1987', category_objects[3], 'https://www.youtube.com/watch?v=ATWBpHq4AlU', '2345', '11:00-23:00 Poniedziałek - Niedziela', 'Lechicka 18, 02-156 Warszawa', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d313060.54258823965!2d20.56640684501387!3d52.192771778110064!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4719334fc72a3d55%3A0x6beaa3e1809c6657!2sTelepizza!5e0!3m2!1spl!2spl!4v1716833853358!5m2!1spl!2spl'),
            ('Restauracja Sejmowa', 'Stołówka w sejmie RP', category_objects[2], 'https://www.youtube.com/watch?v=ZdrWLjuaDp0', '3456', '08:00–21:00 Poniedziałek - Piątek', 'Senacka, 00-487 Warszawa', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2443.9466213338014!2d21.022667297226782!3d52.226187585712594!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x471ecd07367c6b01%3A0x7356794197efa1b9!2sRestauracja%20Sejmowa!5e0!3m2!1spl!2spl!4v1716833985440!5m2!1spl!2spl'),
            ('U Fukiera', 'Restauracja Magdy Gessler', category_objects[0], 'https://www.youtube.com/watch?v=iVG3kXZ51eI', '4567', '12:00–23:00 Poniedziałek - Niedziela', 'Rynek Starego Miasta 27, 00-272 Warszawa', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2442.652212771164!2d21.009033777554308!3d52.24970045620545!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x471ecc6f6e6d4c4d%3A0x23657e12532da664!2sU%20Fukiera!5e0!3m2!1spl!2spl!4v1716834113163!5m2!1spl!2spl')
        ]

        for name, description, category, video_url, visit_code, open_hours, localization, iframe_link in venues:
            Venue.objects.create(name=name, description=description, category=category, video_url=video_url, visit_code=visit_code, open_hours=open_hours, localization=localization, iframe_link=iframe_link)

        self.stdout.write(self.style.SUCCESS('Successfully added test venues.'))
