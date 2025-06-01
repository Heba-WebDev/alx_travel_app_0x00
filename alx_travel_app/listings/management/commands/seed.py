from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import uuid
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample users, listings, bookings, and reviews'

    def handle(self, *args, **kwargs):
        # Clear previous data (if needed)
        #Review.objects.all().delete()
        #Booking.objects.all().delete()
        #Listing.objects.all().delete()
        #User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Seeding users...")
        hosts = []
        travelers = []

        for i in range(3):
            host = User.objects.create_user(
                username=f"host{i}",
                email=f"host{i}@mail.com",
                password="testpass123",
                is_host=True
            )
            hosts.append(host)

        for i in range(5):
            user = User.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@mail.com",
                password="testpass123",
                is_host=False
            )
            travelers.append(user)

        self.stdout.write("Seeding listings...")
        listings = []
        for i in range(5):
            listing = Listing.objects.create(
                id=uuid.uuid4(),
                title=f"Sample Listing {i}",
                description="A cozy place to stay.",
                location=random.choice(["Paris", "Tokyo", "Berlin", "Nairobi", "Rio"]),
                price_per_night=random.uniform(50, 200),
                max_guests=random.randint(1, 6),
                host=random.choice(hosts)
            )
            listings.append(listing)

        self.stdout.write("Seeding bookings...")
        bookings = []
        for i in range(8):
            check_in = timezone.now().date() + timedelta(days=random.randint(1, 30))
            check_out = check_in + timedelta(days=random.randint(1, 5))
            booking = Booking.objects.create(
                id=uuid.uuid4(),
                listing=random.choice(listings),
                user=random.choice(travelers),
                check_in=check_in,
                check_out=check_out
            )
            bookings.append(booking)

        self.stdout.write("Seeding reviews...")
        for booking in random.sample(bookings, k=min(len(bookings), 5)):
            Review.objects.create(
                id=uuid.uuid4(),
                booking=booking,
                rating=random.randint(1, 5),
                comment=random.choice([
                    "Excellent stay!", "Pretty good overall.", "It was okay.",
                    "Not great, could be cleaner.", "Worst experience ever."
                ])
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded all models!"))
