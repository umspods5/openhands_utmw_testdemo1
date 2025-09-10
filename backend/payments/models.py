from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid

User = get_user_model()

class PaymentMethod(models.Model):
    PAYMENT_TYPES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Digital Wallet'),
        ('cash', 'Cash'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    
    # Card details (encrypted)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)  # Visa, MasterCard, etc.
    card_expiry_month = models.IntegerField(null=True, blank=True)
    card_expiry_year = models.IntegerField(null=True, blank=True)
    
    # UPI details
    upi_id = models.CharField(max_length=100, blank=True)
    
    # Wallet details
    wallet_provider = models.CharField(max_length=50, blank=True)  # Paytm, PhonePe, etc.
    
    # Bank details
    bank_name = models.CharField(max_length=100, blank=True)
    account_holder_name = models.CharField(max_length=100, blank=True)
    
    # Razorpay integration
    razorpay_payment_method_id = models.CharField(max_length=100, blank=True)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.payment_type in ['credit_card', 'debit_card']:
            return f"{self.card_brand} ending in {self.card_last_four}"
        elif self.payment_type == 'upi':
            return f"UPI: {self.upi_id}"
        else:
            return f"{self.get_payment_type_display()}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('booking_payment', 'Booking Payment'),
        ('locker_rental', 'Locker Rental'),
        ('penalty', 'Late Collection Penalty'),
        ('refund', 'Refund'),
        ('security_deposit', 'Security Deposit'),
        ('maintenance_fee', 'Maintenance Fee'),
    )
    
    TRANSACTION_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    )
    
    PAYMENT_GATEWAYS = (
        ('razorpay', 'Razorpay'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
        ('gpay', 'Google Pay'),
        ('cash', 'Cash'),
    )
    
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=30, choices=TRANSACTION_STATUS, default='pending')
    
    # Amount details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    
    # Payment gateway details
    payment_gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAYS)
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    gateway_order_id = models.CharField(max_length=100, blank=True)
    gateway_payment_id = models.CharField(max_length=100, blank=True)
    
    # Payment method used
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Fees and charges
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    gateway_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Refund details
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    refund_reason = models.TextField(blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    
    # Error handling
    failure_reason = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.user.username} - ₹{self.amount} - {self.status}"

class PaymentPlan(models.Model):
    PLAN_TYPES = (
        ('pay_per_use', 'Pay Per Use'),
        ('monthly', 'Monthly Subscription'),
        ('quarterly', 'Quarterly Subscription'),
        ('yearly', 'Yearly Subscription'),
        ('enterprise', 'Enterprise Plan'),
    )
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    description = models.TextField()
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    per_use_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Limits
    monthly_usage_limit = models.IntegerField(null=True, blank=True)  # Number of bookings
    storage_time_limit = models.IntegerField(default=24)  # Hours
    
    # Features
    includes_refrigeration = models.BooleanField(default=False)
    includes_heating = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    extended_storage = models.BooleanField(default=False)
    
    # Discounts
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - ₹{self.base_price}"

class UserSubscription(models.Model):
    SUBSCRIPTION_STATUS = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='subscriptions')
    
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='active')
    
    # Usage tracking
    current_usage = models.IntegerField(default=0)
    usage_reset_date = models.DateTimeField()
    
    # Subscription period
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    # Auto-renewal
    auto_renew = models.BooleanField(default=True)
    next_billing_date = models.DateTimeField(null=True, blank=True)
    
    # Payment tracking
    last_payment = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscription_payments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"

class Invoice(models.Model):
    INVOICE_STATUS = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )
    
    invoice_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='invoice')
    
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    
    # Invoice details
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('18.00'))  # GST
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment tracking
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # File storage
    pdf_file = models.FileField(upload_to='invoices/', blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.user.username} - ₹{self.total_amount}"

class PaymentWebhook(models.Model):
    WEBHOOK_EVENTS = (
        ('payment.authorized', 'Payment Authorized'),
        ('payment.captured', 'Payment Captured'),
        ('payment.failed', 'Payment Failed'),
        ('order.paid', 'Order Paid'),
        ('refund.created', 'Refund Created'),
        ('subscription.charged', 'Subscription Charged'),
    )
    
    webhook_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=50, choices=WEBHOOK_EVENTS)
    gateway = models.CharField(max_length=20)
    
    # Payload data
    raw_payload = models.JSONField()
    processed_payload = models.JSONField(default=dict, blank=True)
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    
    # Related objects
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='webhooks')
    
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.event_type} - {self.webhook_id} - {self.is_processed}"
