# Django Listings Application

This project is a Django-based application for managing listings, bookings, and reviews. The setup includes models, serializers, and seeders to populate the database with sample data for testing purposes.

## Features

- **Listings**: Create and manage listings with details like name, description, price per night, and location.
- **Bookings**: Allow users to book listings with defined start and end dates.
- **Reviews**: Enable users to leave reviews with ratings and comments for listings.

## Setup Instructions

### 1. Define Models

Add the following models in `listings/models.py`:

#### Listing Model
```python
class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

#### Booking Model
```python
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.listing.name}"
```

#### Review Model
```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.listing.name}"
```

---

### 2. Set Up Serializers

Create serializers for the `Listing` and `Booking` models in `listings/serializers.py`:

#### Listing Serializer
```python
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
```

#### Booking Serializer
```python
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
```

---

### 3. Implement Seeders

#### Create Seeder Command

1. Create the directory structure `listings/management/commands` if it does not exist.
2. Add a `seed.py` file in `commands/` with the following code:

```python
import random
from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    help = 'Seed the database with sample listings data'

    def handle(self, *args, **kwargs):
        sample_listings = [
            {
                "name": "Cozy Cottage",
                "description": "A charming cottage in the countryside.",
                "price_per_night": random.uniform(50, 150),
                "location": "Countryside"
            },
            {
                "name": "Modern Apartment",
                "description": "A sleek and modern apartment in the city center.",
                "price_per_night": random.uniform(100, 300),
                "location": "City Center"
            },
            {
                "name": "Beachfront Villa",
                "description": "A luxurious villa right on the beach.",
                "price_per_night": random.uniform(200, 500),
                "location": "Beach"
            },
        ]

        for listing_data in sample_listings:
            Listing.objects.create(**listing_data)

        self.stdout.write(self.style.SUCCESS("Successfully seeded the database with sample listings data."))
```

---

### 4. Run the Seeder

#### Apply Migrations
Run the following commands to apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Populate the Database
Run the seeder command to populate the database with sample listings:
```bash
python manage.py seed
```

---

### 5. Verify

- Use the Django admin panel to view the `Listing`, `Booking`, and `Review` entries.
- Alternatively, test your API endpoints to confirm the seeded data is accessible.

---

## Additional Notes

- Ensure you have the `User` model set up correctly for handling `ForeignKey` relationships.
- Modify sample data as required for testing.
- Extend serializers and views to include `Review` functionality if needed.
