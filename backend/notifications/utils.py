"""
Utility functions for WhatsApp messaging and AI bot integration.
These functions provide easy-to-use interfaces for common messaging tasks.
"""

import logging
from typing import Dict, Optional, List
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import (
    WhatsAppSession, WhatsAppMessage, AIBotConfiguration, 
    OTPVerification, Notification, NotificationTemplate
)
from .services import WhatsAppAutomationService, AIBotService, NotificationService
from .tasks import (
    send_notification_task, generate_ai_otp, send_otp_whatsapp,
    process_whatsapp_responses
)

User = get_user_model()
logger = logging.getLogger(__name__)


class WhatsAppMessenger:
    """
    High-level interface for WhatsApp messaging operations.
    Handles session management and provides simple methods for common tasks.
    """
    
    def __init__(self):
        self.service = WhatsAppAutomationService()
        self.session = None
        
    def ensure_active_session(self) -> bool:
        """Ensure there's an active WhatsApp session."""
        self.session = WhatsAppSession.objects.filter(status='active').first()
        
        if not self.session:
            logger.error("No active WhatsApp session found")
            return False
            
        self.service.session = self.session
        return True
    
    def send_quick_message(self, phone_number: str, message: str) -> bool:
        """Send a quick message without creating notification records."""
        if not self.ensure_active_session():
            return False
            
        self.service.initialize_driver(headless=True)
        success = self.service.send_message(phone_number, message)
        self.service.close_session()
        
        return success
    
    def send_otp(self, phone_number: str, user_id: int, otp_type: str = 'verification') -> Optional[str]:
        """Generate and send OTP to user."""
        try:
            user = User.objects.get(id=user_id)
            
            # Generate OTP using AI if available
            ai_bot = AIBotConfiguration.objects.filter(
                purpose='otp_generation',
                is_active=True
            ).first()
            
            ai_service = AIBotService()
            
            if ai_bot:
                if ai_bot.provider == 'openai':
                    ai_service.initialize_openai(ai_bot.api_key)
                elif ai_bot.provider == 'google':
                    ai_service.initialize_gemini(ai_bot.api_key)
                
                otp_code = ai_service.generate_otp(length=6, use_ai=True)
            else:
                otp_code = ai_service.generate_otp(length=6, use_ai=False)
            
            # Create OTP verification record
            otp_verification = OTPVerification.objects.create(
                user=user,
                otp_type=otp_type,
                otp_code=otp_code,
                phone_number=phone_number,
                expires_at=timezone.now() + timedelta(minutes=10),
                generated_by_ai=bool(ai_bot),
                ai_bot=ai_bot
            )
            
            # Send OTP via WhatsApp
            if not self.ensure_active_session():
                return None
                
            self.service.initialize_driver(headless=True)
            success = self.service.send_otp_message(phone_number, otp_code, otp_type)
            self.service.close_session()
            
            if success:
                otp_verification.status = 'sent'
                otp_verification.sent_at = timezone.now()
                otp_verification.save()
                return otp_code
            else:
                otp_verification.status = 'failed'
                otp_verification.save()
                return None
                
        except Exception as e:
            logger.error(f"Error sending OTP: {e}")
            return None
    
    def send_parcel_approval_request(self, phone_number: str, booking_details: Dict) -> bool:
        """Send parcel approval request to customer."""
        if not self.ensure_active_session():
            return False
            
        self.service.initialize_driver(headless=True)
        success = self.service.send_approval_request(phone_number, booking_details)
        self.service.close_session()
        
        return success
    
    def check_user_response(self, phone_number: str) -> Optional[str]:
        """Check for user response in WhatsApp chat."""
        if not self.ensure_active_session():
            return None
            
        self.service.initialize_driver(headless=True)
        response = self.service.check_for_responses(phone_number)
        self.service.close_session()
        
        return response


class SmartNotificationManager:
    """
    Manager for creating and sending smart notifications with AI personalization.
    """
    
    def __init__(self):
        self.notification_service = NotificationService()
        self.ai_service = AIBotService()
    
    def send_personalized_notification(
        self, 
        user: User, 
        template_type: str, 
        channel: str = 'whatsapp',
        context_data: Dict = None,
        priority: str = 'medium'
    ) -> bool:
        """
        Send a personalized notification using AI.
        """
        try:
            # Get notification template
            template = NotificationTemplate.objects.filter(
                template_type=template_type,
                channel=channel,
                is_active=True
            ).first()
            
            if not template:
                logger.error(f"No template found for {template_type} - {channel}")
                return False
            
            # Prepare user data for personalization
            user_data = {
                'name': user.get_full_name() or user.username,
                'username': user.username,
                'email': user.email,
                'phone': getattr(user, 'phone_number', ''),
                **(context_data or {})
            }
            
            # Get AI bot for message personalization
            ai_bot = AIBotConfiguration.objects.filter(
                purpose='message_personalization',
                is_active=True
            ).first()
            
            # Personalize message
            if ai_bot:
                if ai_bot.provider == 'openai':
                    self.ai_service.initialize_openai(ai_bot.api_key)
                elif ai_bot.provider == 'google':
                    self.ai_service.initialize_gemini(ai_bot.api_key)
                
                personalized_message = self.ai_service.personalize_message(
                    template.message_template, 
                    user_data, 
                    ai_bot
                )
            else:
                personalized_message = self.ai_service._simple_template_substitution(
                    template.message_template, 
                    user_data
                )
            
            # Create notification
            notification = Notification.objects.create(
                recipient=user,
                template=template,
                subject=template.subject,
                message=personalized_message,
                recipient_phone=getattr(user, 'phone_number', ''),
                recipient_email=user.email,
                priority=priority,
                metadata=context_data or {}
            )
            
            # Send notification asynchronously
            send_notification_task.delay(str(notification.notification_id))
            
            return True
            
        except Exception as e:
            logger.error(f"Error sending personalized notification: {e}")
            return False
    
    def bulk_send_notifications(
        self, 
        users: List[User], 
        template_type: str, 
        channel: str = 'whatsapp',
        context_data: Dict = None
    ) -> int:
        """
        Send notifications to multiple users.
        Returns the number of successfully queued notifications.
        """
        success_count = 0
        
        for user in users:
            if self.send_personalized_notification(
                user, template_type, channel, context_data
            ):
                success_count += 1
        
        return success_count


class OTPManager:
    """
    Manager for OTP operations with AI integration.
    """
    
    @staticmethod
    def generate_and_send_otp(
        user: User, 
        phone_number: str, 
        otp_type: str = 'verification'
    ) -> Optional[str]:
        """Generate and send OTP to user."""
        messenger = WhatsAppMessenger()
        return messenger.send_otp(phone_number, user.id, otp_type)
    
    @staticmethod
    def verify_otp(user: User, otp_code: str, otp_type: str = 'verification') -> bool:
        """Verify OTP code."""
        try:
            otp_verification = OTPVerification.objects.filter(
                user=user,
                otp_code=otp_code,
                otp_type=otp_type,
                status='sent',
                expires_at__gt=timezone.now()
            ).first()
            
            if not otp_verification:
                return False
            
            # Check attempt limits
            if otp_verification.verification_attempts >= otp_verification.max_attempts:
                otp_verification.status = 'failed'
                otp_verification.save()
                return False
            
            # Increment attempts
            otp_verification.verification_attempts += 1
            
            # Verify OTP
            if otp_verification.otp_code == otp_code:
                otp_verification.status = 'verified'
                otp_verification.verified_at = timezone.now()
                otp_verification.save()
                return True
            else:
                otp_verification.save()
                return False
                
        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            return False
    
    @staticmethod
    def resend_otp(user: User, phone_number: str, otp_type: str = 'verification') -> Optional[str]:
        """Resend OTP to user."""
        # Mark previous OTPs as expired
        OTPVerification.objects.filter(
            user=user,
            otp_type=otp_type,
            status__in=['generated', 'sent']
        ).update(status='expired')
        
        # Generate and send new OTP
        return OTPManager.generate_and_send_otp(user, phone_number, otp_type)


class BookingNotificationHelper:
    """
    Helper class for booking-related notifications.
    """
    
    @staticmethod
    def send_booking_confirmation(booking) -> bool:
        """Send booking confirmation to customer."""
        manager = SmartNotificationManager()
        
        context_data = {
            'booking_id': str(booking.booking_id),
            'item_description': booking.item_description,
            'sender_name': booking.sender_name,
            'recipient_apartment': booking.recipient_apartment,
            'estimated_delivery': booking.estimated_delivery_time.strftime('%Y-%m-%d %H:%M') if booking.estimated_delivery_time else 'TBD'
        }
        
        return manager.send_personalized_notification(
            booking.customer,
            'booking_confirmation',
            'whatsapp',
            context_data,
            'high'
        )
    
    @staticmethod
    def send_delivery_approval_request(booking) -> bool:
        """Send delivery approval request to customer."""
        messenger = WhatsAppMessenger()
        
        booking_details = {
            'recipient_name': booking.recipient_name,
            'sender_name': booking.sender_name,
            'item_description': booking.item_description,
            'recipient_apartment': booking.recipient_apartment
        }
        
        return messenger.send_parcel_approval_request(
            booking.recipient_phone,
            booking_details
        )
    
    @staticmethod
    def send_locker_assignment_notification(booking, access_code: str) -> bool:
        """Send locker assignment notification to customer."""
        manager = SmartNotificationManager()
        
        context_data = {
            'booking_id': str(booking.booking_id),
            'locker_location': booking.locker.locker_bank.location_description,
            'locker_number': booking.locker.locker_number,
            'access_code': access_code,
            'expiry_time': '24 hours'
        }
        
        return manager.send_personalized_notification(
            booking.customer,
            'delivery_update',
            'whatsapp',
            context_data,
            'urgent'
        )


# Convenience functions for quick access
def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """Quick function to send WhatsApp message."""
    messenger = WhatsAppMessenger()
    return messenger.send_quick_message(phone_number, message)


def send_otp_to_user(user: User, phone_number: str, otp_type: str = 'verification') -> Optional[str]:
    """Quick function to send OTP to user."""
    return OTPManager.generate_and_send_otp(user, phone_number, otp_type)


def verify_user_otp(user: User, otp_code: str, otp_type: str = 'verification') -> bool:
    """Quick function to verify user OTP."""
    return OTPManager.verify_otp(user, otp_code, otp_type)


def check_whatsapp_responses():
    """Quick function to check for WhatsApp responses."""
    process_whatsapp_responses.delay()