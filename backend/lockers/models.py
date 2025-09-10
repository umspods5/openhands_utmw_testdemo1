from django.db import models
from accounts.models import Building
import uuid

class LockerBank(models.Model):
    bank_id = models.CharField(max_length=20, unique=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='locker_banks')
    location_description = models.CharField(max_length=200)  # e.g., "Ground Floor Lobby"
    total_lockers = models.IntegerField()
    is_active = models.BooleanField(default=True)
    hardware_id = models.CharField(max_length=50, unique=True)  # Arduino/STM32 device ID
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bank_id} - {self.building.name}"

class Locker(models.Model):
    LOCKER_SIZES = (
        ('small', 'Small (20x20x30 cm)'),
        ('medium', 'Medium (30x30x40 cm)'),
        ('large', 'Large (40x40x50 cm)'),
        ('extra_large', 'Extra Large (50x50x60 cm)'),
    )
    
    LOCKER_TYPES = (
        ('standard', 'Standard'),
        ('refrigerated', 'Refrigerated'),
        ('heated', 'Heated'),
        ('document', 'Document Safe'),
    )
    
    LOCKER_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
        ('out_of_order', 'Out of Order'),
    )
    
    locker_bank = models.ForeignKey(LockerBank, on_delete=models.CASCADE, related_name='lockers')
    locker_number = models.CharField(max_length=10)
    size = models.CharField(max_length=20, choices=LOCKER_SIZES)
    locker_type = models.CharField(max_length=20, choices=LOCKER_TYPES, default='standard')
    status = models.CharField(max_length=20, choices=LOCKER_STATUS, default='available')
    current_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    target_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_door_open = models.BooleanField(default=False)
    is_occupied = models.BooleanField(default=False)
    weight_sensor_reading = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    last_opened = models.DateTimeField(null=True, blank=True)
    last_closed = models.DateTimeField(null=True, blank=True)
    hardware_pin = models.IntegerField()  # GPIO pin number for door control
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['locker_bank', 'locker_number']
    
    def __str__(self):
        return f"{self.locker_bank.bank_id}-{self.locker_number}"

class LockerAccess(models.Model):
    ACCESS_TYPES = (
        ('qr_code', 'QR Code'),
        ('otp', 'OTP'),
        ('biometric', 'Biometric'),
        ('manual', 'Manual Override'),
    )
    
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE, related_name='access_logs')
    access_code = models.CharField(max_length=100)  # QR code, OTP, or biometric hash
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPES)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='created_access_codes')
    used_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True, related_name='used_access_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.locker} - {self.access_type} - {self.access_code[:10]}..."

class LockerMaintenance(models.Model):
    MAINTENANCE_TYPES = (
        ('routine', 'Routine Maintenance'),
        ('repair', 'Repair'),
        ('cleaning', 'Cleaning'),
        ('calibration', 'Sensor Calibration'),
        ('upgrade', 'Hardware Upgrade'),
    )
    
    MAINTENANCE_STATUS = (
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS, default='scheduled')
    description = models.TextField()
    scheduled_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    technician = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='maintenance_tasks')
    notes = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.locker} - {self.maintenance_type} - {self.status}"
