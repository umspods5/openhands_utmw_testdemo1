from django.db import models
from django.contrib.auth import get_user_model
from lockers.models import Locker
import uuid

User = get_user_model()

class Booking(models.Model):
    BOOKING_TYPES = (
        ('parcel', 'Parcel Delivery'),
        ('document', 'Document Exchange'),
        ('laundry', 'Laundry Service'),
        ('food_hot', 'Hot Food Delivery'),
        ('food_cold', 'Cold Food Delivery'),
        ('grocery', 'Grocery Delivery'),
        ('other', 'Other'),
    )
    
    BOOKING_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered to Locker'),
        ('collected', 'Collected by Recipient'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )
    
    PRIORITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # User relationships
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    delivery_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_bookings')
    
    # Locker assignment
    locker = models.ForeignKey(Locker, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    # Delivery details
    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=17)
    sender_email = models.EmailField(blank=True)
    
    recipient_name = models.CharField(max_length=100)
    recipient_phone = models.CharField(max_length=17)
    recipient_email = models.EmailField(blank=True)
    recipient_apartment = models.CharField(max_length=10)
    
    # Item details
    item_description = models.TextField()
    item_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    item_weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    requires_refrigeration = models.BooleanField(default=False)
    requires_heating = models.BooleanField(default=False)
    target_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Timing
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    collection_deadline = models.DateTimeField()
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    
    # Special instructions
    special_instructions = models.TextField(blank=True)
    fragile = models.BooleanField(default=False)
    
    # Tracking
    tracking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    qr_code = models.CharField(max_length=100, null=True, blank=True)
    access_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.booking_id} - {self.booking_type} - {self.status}"

class BookingStatusHistory(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.booking.booking_id} - {self.previous_status} to {self.new_status}"

class BookingPhoto(models.Model):
    PHOTO_TYPES = (
        ('pickup', 'Pickup Photo'),
        ('delivery', 'Delivery Photo'),
        ('damage', 'Damage Photo'),
        ('proof', 'Proof of Delivery'),
    )
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='photos')
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPES)
    image = models.ImageField(upload_to='booking_photos/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.booking.booking_id} - {self.photo_type}"

class DeliveryRoute(models.Model):
    ROUTE_STATUS = (
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    delivery_agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_routes')
    route_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=ROUTE_STATUS, default='planned')
    total_bookings = models.IntegerField(default=0)
    completed_bookings = models.IntegerField(default=0)
    estimated_duration = models.DurationField(null=True, blank=True)
    actual_duration = models.DurationField(null=True, blank=True)
    total_distance = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.route_name} - {self.delivery_agent.get_full_name()}"

class RouteBooking(models.Model):
    route = models.ForeignKey(DeliveryRoute, on_delete=models.CASCADE, related_name='route_bookings')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='route_assignments')
    sequence_order = models.IntegerField()
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['route', 'booking']
        ordering = ['sequence_order']
    
    def __str__(self):
        return f"{self.route.route_name} - {self.booking.booking_id} - #{self.sequence_order}"
