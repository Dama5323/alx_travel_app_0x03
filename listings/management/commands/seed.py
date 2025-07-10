from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample listings
        listings = [
            {'name': 'Beach House', 'description': 'A beautiful house by the beach', 'price_per_night': 120.50},
            {'name': 'Mountain Cabin', 'description': 'A cozy cabin in the mountains', 'price_per_night': 80.00},
        ]

        for listing_data in listings:
            Listing.objects.create(**listing_data)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))