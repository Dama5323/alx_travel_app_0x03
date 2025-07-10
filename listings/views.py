from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
from .tasks import send_booking_confirmation_email


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

@api_view(['POST'])
def initiate_payment(request):
    data = request.data
    chapa_url = "https://api.chapa.co/v1/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount": data["amount"],
        "currency": "ETB",
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "tx_ref": data["booking_reference"],
        "callback_url": "http://your-domain.com/api/verify-payment/"
    }

    response = requests.post(chapa_url, headers=headers, json=payload)
    resp_data = response.json()

    if resp_data.get("status") == "success":
        Payment.objects.create(
            booking_reference=data["booking_reference"],
            transaction_id=resp_data["data"]["tx_ref"],
            amount=data["amount"],
            status="Pending"
        )
        return Response({"checkout_url": resp_data["data"]["checkout_url"]})
    else:
        return Response({"error": "Payment initiation failed"}, status=400)
    
@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.query_params.get("tx_ref")
    verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }
    response = requests.get(verify_url, headers=headers)
    resp_data = response.json()

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
        if resp_data["status"] == "success" and resp_data["data"]["status"] == "success":
            payment.status = "Completed"
        else:
            payment.status = "Failed"
        payment.save()
        return Response({"message": "Payment status updated", "status": payment.status})
    except Payment.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)
    
def perform_create(self, serializer):
    booking = serializer.save()
    email = booking.user.email  # Adjust if your model is different
    details = f"Destination: {booking.destination}\nDate: {booking.date}"
    
    # Trigger background task
    send_booking_confirmation_email.delay(email, details)


