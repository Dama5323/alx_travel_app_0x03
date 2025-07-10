from rest_framework import serializers
from .models import Listing, Booking, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for the Listing model."""
    host = serializers.ReadOnlyField(source='host.username')

    class Meta:
        model = Listing
        fields = [
            'id', 
            'title', 
            'description', 
            'price_per_night', 
            'location', 
            'host', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'host', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for the Booking model."""
    guest = serializers.ReadOnlyField(source='guest.username')
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = [
            'id', 
            'listing', 
            'guest', 
            'check_in_date', 
            'check_out_date', 
            'total_price', 
            'created_at'
        ]
        read_only_fields = ['id', 'guest', 'total_price', 'created_at']

    def validate(self, data):
        """Custom validation to ensure check_out_date is after check_in_date."""
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )
        return data

    def create(self, validated_data):
        """Automatically calculate total price based on booking duration."""
        listing = validated_data['listing']
        check_in_date = validated_data['check_in_date']
        check_out_date = validated_data['check_out_date']

        # Calculate total price
        nights = (check_out_date - check_in_date).days
        total_price = listing.price_per_night * nights

        # Create booking instance
        booking = Booking.objects.create(
            listing=listing,
            guest=self.context['request'].user,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_price=total_price
        )
        return booking