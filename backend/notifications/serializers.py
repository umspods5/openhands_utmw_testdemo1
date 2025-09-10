from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    NotificationTemplate, Notification, WhatsAppSession, WhatsAppMessage,
    AIBotConfiguration, AIBotInteraction, OTPVerification
)

User = get_user_model()


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'notification_id', 'recipient', 'recipient_username', 'template', 
            'template_name', 'subject', 'message', 'recipient_phone', 
            'recipient_email', 'status', 'priority', 'scheduled_at', 
            'sent_at', 'delivered_at', 'read_at', 'retry_count', 
            'max_retries', 'error_message', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = ['notification_id', 'created_at', 'updated_at']


class WhatsAppSessionSerializer(serializers.ModelSerializer):
    messages_count = serializers.SerializerMethodField()
    
    class Meta:
        model = WhatsAppSession
        fields = [
            'id', 'session_id', 'phone_number', 'status', 'qr_code_path',
            'last_activity', 'session_data', 'error_message', 'messages_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['session_id', 'created_at', 'updated_at']
    
    def get_messages_count(self, obj):
        return obj.messages.count()


class WhatsAppMessageSerializer(serializers.ModelSerializer):
    notification_id = serializers.CharField(source='notification.notification_id', read_only=True)
    session_phone = serializers.CharField(source='session.phone_number', read_only=True)
    
    class Meta:
        model = WhatsAppMessage
        fields = [
            'id', 'notification', 'notification_id', 'session', 'session_phone',
            'recipient_phone', 'message_type', 'message_content', 'requires_response',
            'response_options', 'user_response', 'response_received_at', 'status',
            'whatsapp_message_id', 'sent_at', 'delivered_at', 'read_at',
            'error_message', 'retry_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AIBotConfigurationSerializer(serializers.ModelSerializer):
    interactions_count = serializers.SerializerMethodField()
    usage_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = AIBotConfiguration
        fields = [
            'id', 'name', 'provider', 'purpose', 'api_endpoint', 'api_key',
            'model_name', 'max_tokens', 'temperature', 'daily_limit',
            'monthly_limit', 'current_daily_usage', 'current_monthly_usage',
            'interactions_count', 'usage_percentage', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True}  # Don't expose API keys in responses
        }
    
    def get_interactions_count(self, obj):
        return obj.interactions.count()
    
    def get_usage_percentage(self, obj):
        if obj.daily_limit > 0:
            return round((obj.current_daily_usage / obj.daily_limit) * 100, 2)
        return 0


class AIBotInteractionSerializer(serializers.ModelSerializer):
    bot_name = serializers.CharField(source='bot_config.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AIBotInteraction
        fields = [
            'id', 'bot_config', 'bot_name', 'user', 'user_username',
            'interaction_type', 'input_text', 'context_data', 'output_text',
            'tokens_used', 'response_time', 'is_successful', 'error_message',
            'created_at'
        ]
        read_only_fields = ['created_at']


class OTPVerificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    ai_bot_name = serializers.CharField(source='ai_bot.name', read_only=True)
    is_expired = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = OTPVerification
        fields = [
            'id', 'user', 'user_username', 'otp_type', 'otp_code',
            'phone_number', 'status', 'generated_by_ai', 'ai_bot',
            'ai_bot_name', 'generated_at', 'sent_at', 'verified_at',
            'expires_at', 'verification_attempts', 'max_attempts',
            'is_expired', 'time_remaining', 'metadata'
        ]
        read_only_fields = ['generated_at']
        extra_kwargs = {
            'otp_code': {'write_only': True}  # Don't expose OTP codes in responses
        }
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.expires_at < timezone.now()
    
    def get_time_remaining(self, obj):
        from django.utils import timezone
        if obj.expires_at > timezone.now():
            remaining = obj.expires_at - timezone.now()
            return int(remaining.total_seconds())
        return 0


class OTPVerificationCreateSerializer(serializers.Serializer):
    """Serializer for creating OTP verification requests."""
    phone_number = serializers.CharField(max_length=17)
    user_id = serializers.IntegerField(required=False)
    otp_type = serializers.ChoiceField(
        choices=OTPVerification.OTP_TYPES,
        default='verification'
    )


class OTPVerifySerializer(serializers.Serializer):
    """Serializer for verifying OTP codes."""
    user_id = serializers.IntegerField()
    otp_code = serializers.CharField(max_length=10)
    otp_type = serializers.ChoiceField(
        choices=OTPVerification.OTP_TYPES,
        default='verification'
    )


class WhatsAppMessageCreateSerializer(serializers.Serializer):
    """Serializer for creating WhatsApp messages."""
    phone_number = serializers.CharField(max_length=17)
    message = serializers.CharField()
    message_type = serializers.ChoiceField(
        choices=WhatsAppMessage.MESSAGE_TYPES,
        default='text'
    )


class ApprovalRequestSerializer(serializers.Serializer):
    """Serializer for parcel approval requests."""
    phone_number = serializers.CharField(max_length=17)
    booking_details = serializers.DictField()
    
    def validate_booking_details(self, value):
        """Validate booking details structure."""
        required_fields = ['recipient_name', 'sender_name', 'item_description']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"Missing required field: {field}")
        return value


class PersonalizedNotificationSerializer(serializers.Serializer):
    """Serializer for personalized notifications."""
    user_id = serializers.IntegerField()
    template_type = serializers.ChoiceField(choices=NotificationTemplate.TEMPLATE_TYPES)
    channel = serializers.ChoiceField(
        choices=NotificationTemplate.CHANNELS,
        default='whatsapp'
    )
    context_data = serializers.DictField(default=dict)
    priority = serializers.ChoiceField(
        choices=Notification.PRIORITY_LEVELS,
        default='medium'
    )


class WhatsAppStatusSerializer(serializers.Serializer):
    """Serializer for WhatsApp system status."""
    active_sessions = serializers.IntegerField()
    recent_messages_24h = serializers.IntegerField()
    pending_approvals = serializers.IntegerField()
    active_ai_bots = serializers.IntegerField()
    system_status = serializers.CharField()


class BulkNotificationSerializer(serializers.Serializer):
    """Serializer for bulk notifications."""
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    template_type = serializers.ChoiceField(choices=NotificationTemplate.TEMPLATE_TYPES)
    channel = serializers.ChoiceField(
        choices=NotificationTemplate.CHANNELS,
        default='whatsapp'
    )
    context_data = serializers.DictField(default=dict)
    priority = serializers.ChoiceField(
        choices=Notification.PRIORITY_LEVELS,
        default='medium'
    )