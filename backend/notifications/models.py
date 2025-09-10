from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class NotificationTemplate(models.Model):
    TEMPLATE_TYPES = (
        ('otp_verification', 'OTP Verification'),
        ('booking_confirmation', 'Booking Confirmation'),
        ('delivery_update', 'Delivery Update'),
        ('parcel_approval', 'Parcel Approval Request'),
        ('collection_reminder', 'Collection Reminder'),
        ('payment_confirmation', 'Payment Confirmation'),
        ('maintenance_alert', 'Maintenance Alert'),
        ('system_notification', 'System Notification'),
    )
    
    CHANNELS = (
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
    )
    
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES)
    channel = models.CharField(max_length=20, choices=CHANNELS)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200, blank=True)  # For email
    message_template = models.TextField()
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['template_type', 'channel', 'language']
    
    def __str__(self):
        return f"{self.name} - {self.channel}"

class Notification(models.Model):
    NOTIFICATION_STATUS = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    PRIORITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    notification_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    
    # Message content
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    
    # Delivery details
    recipient_phone = models.CharField(max_length=17, blank=True)
    recipient_email = models.EmailField(blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Retry mechanism
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    
    # Error tracking
    error_message = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.notification_id} - {self.recipient.username} - {self.template.name}"

class WhatsAppSession(models.Model):
    SESSION_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
        ('error', 'Error'),
    )
    
    session_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=17)  # Business WhatsApp number
    status = models.CharField(max_length=20, choices=SESSION_STATUS, default='inactive')
    qr_code_path = models.CharField(max_length=500, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    session_data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"WhatsApp Session - {self.phone_number} - {self.status}"

class WhatsAppMessage(models.Model):
    MESSAGE_STATUS = (
        ('queued', 'Queued'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    )
    
    MESSAGE_TYPES = (
        ('text', 'Text Message'),
        ('otp', 'OTP Message'),
        ('approval', 'Approval Request'),
        ('reminder', 'Reminder'),
        ('confirmation', 'Confirmation'),
    )
    
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name='whatsapp_message')
    session = models.ForeignKey(WhatsAppSession, on_delete=models.CASCADE, related_name='messages')
    
    recipient_phone = models.CharField(max_length=17)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    message_content = models.TextField()
    
    # Interactive elements for approval/denial
    requires_response = models.BooleanField(default=False)
    response_options = models.JSONField(default=list, blank=True)  # ['Approve', 'Deny']
    user_response = models.CharField(max_length=50, blank=True)
    response_received_at = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS, default='queued')
    whatsapp_message_id = models.CharField(max_length=100, blank=True)
    
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"WhatsApp to {self.recipient_phone} - {self.message_type} - {self.status}"

class AIBotConfiguration(models.Model):
    BOT_PROVIDERS = (
        ('openai', 'OpenAI GPT'),
        ('google', 'Google Gemini'),
        ('huggingface', 'Hugging Face'),
        ('local', 'Local Model'),
    )
    
    BOT_PURPOSES = (
        ('customer_support', 'Customer Support'),
        ('otp_generation', 'OTP Generation'),
        ('message_personalization', 'Message Personalization'),
        ('response_processing', 'Response Processing'),
        ('language_translation', 'Language Translation'),
    )
    
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=20, choices=BOT_PROVIDERS)
    purpose = models.CharField(max_length=30, choices=BOT_PURPOSES)
    api_endpoint = models.URLField(blank=True)
    api_key = models.CharField(max_length=200, blank=True)
    model_name = models.CharField(max_length=100)
    
    # Configuration parameters
    max_tokens = models.IntegerField(default=150)
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.7)
    
    # Usage limits
    daily_limit = models.IntegerField(default=1000)
    monthly_limit = models.IntegerField(default=30000)
    current_daily_usage = models.IntegerField(default=0)
    current_monthly_usage = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.provider} - {self.purpose}"

class AIBotInteraction(models.Model):
    INTERACTION_TYPES = (
        ('otp_request', 'OTP Request'),
        ('message_generation', 'Message Generation'),
        ('response_analysis', 'Response Analysis'),
        ('translation', 'Translation'),
        ('support_query', 'Support Query'),
    )
    
    bot_config = models.ForeignKey(AIBotConfiguration, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    interaction_type = models.CharField(max_length=30, choices=INTERACTION_TYPES)
    
    # Request details
    input_text = models.TextField()
    context_data = models.JSONField(default=dict, blank=True)
    
    # Response details
    output_text = models.TextField(blank=True)
    tokens_used = models.IntegerField(default=0)
    response_time = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    
    # Status
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.bot_config.name} - {self.interaction_type} - {self.created_at}"

class OTPVerification(models.Model):
    OTP_TYPES = (
        ('registration', 'Registration'),
        ('login', 'Login'),
        ('booking_approval', 'Booking Approval'),
        ('locker_access', 'Locker Access'),
        ('payment', 'Payment Verification'),
    )
    
    OTP_STATUS = (
        ('generated', 'Generated'),
        ('sent', 'Sent'),
        ('verified', 'Verified'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_verifications')
    otp_type = models.CharField(max_length=20, choices=OTP_TYPES)
    otp_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=17)
    
    status = models.CharField(max_length=20, choices=OTP_STATUS, default='generated')
    
    # AI-generated OTP details
    generated_by_ai = models.BooleanField(default=False)
    ai_bot = models.ForeignKey(AIBotConfiguration, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timing
    generated_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    # Verification attempts
    verification_attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=3)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"OTP {self.otp_code} - {self.user.username} - {self.otp_type}"
