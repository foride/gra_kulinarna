from django.core.management.base import BaseCommand
from core.models import Achievement


class Command(BaseCommand):
    help = 'Add predefined achievements to the database'

    def handle(self, *args, **kwargs):
        achievements = [
            # Points Collected
            ("Początkujący Zbieracz Punktów", "Zdobądź 1000 punktów", 1000),
            ("Średniozaawansowany Zbieracz Punktów", "Zdobądź 5000 punktów", 5000),
            ("Zaawansowany Zbieracz Punktów", "Zdobądź 10000 punktów", 10000),

            # Visited Venues
            ("Odkrywca Lokali", "Odwiedź 10 lokali", 10),
            ("Ekspert Lokali", "Odwiedź 50 lokali", 50),
            ("Mistrz Lokali", "Odwiedź 100 lokali", 100),

            # Rated Venues
            ("Początkujący Krytyk", "Oceń 5 lokali", 5),
            ("Średniozaawansowany Krytyk", "Oceń 20 lokali", 20),
            ("Zaawansowany Krytyk", "Oceń 50 lokali", 50),

            # Comments
            ("Aktywny Komentator", "Napisz 10 komentarzy", 10),
            ("Zaangażowany Komentator", "Napisz 50 komentarzy", 50),
            ("Mistrz Dyskusji", "Napisz 100 komentarzy", 100),
        ]

        for name, description, points_required in achievements:
            Achievement.objects.get_or_create(
                name=name,
                description=description,
                points_required=points_required
            )

        self.stdout.write(self.style.SUCCESS('Successfully added predefined achievements.'))
