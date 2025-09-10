from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from .models import (
    Notification, WhatsAppSession, WhatsAppMessage, 
    OTPVerification, AIBotConfiguration
)
from .services import NotificationService, WhatsAppAutomationService, AIBotService

logger = logging.getLogger(__name__)

@shared_task
def send_notification_task(notification_id):
    """
    Celery task to send notifications asynchronously.
    """
    try:
        notification = Notification.objects.get(notification_id=notification_id)
        service = NotificationService()
        
        success = service.send_notification(notification)
        
        if success:
            logger.info(f"Notification {notification_id} sent successfully")
        else:
            logger.error(f"Failed to send notification {notification_id}")
            
        return success
        
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error sending notification {notification_id}: {e}")
        return False

@shared_task
def process_whatsapp_responses():
    """
    Celery task to check for WhatsApp responses and process them.
    """
    try:
        # Get all pending approval messages
        pending_messages = WhatsAppMessage.objects.filter(
            message_type='approval',
            requires_response=True,
            user_response='',
            status='sent'
        )
        
        whatsapp_service = WhatsAppAutomationService()
        
        # Get active session
        session = WhatsAppSession.objects.filter(status='active').first()
        if not session:
            logger.warning("No active WhatsApp session found")
            return
        
        whatsapp_service.session = session
        whatsapp_service.initialize_driver(headless=True)
        
        responses_processed = 0
        
        for message in pending_messages:
            try:
                response = whatsapp_service.check_for_responses(message.recipient_phone)
                
                if response:
                    message.user_response = response
                    message.response_received_at = timezone.now()
                    message.save()
                    
                    # Process the response
                    process_approval_response.delay(message.id, response)
                    responses_processed += 1
                    
            except Exception as e:
                logger.error(f"Error checking response for message {message.id}: {e}")
        
        whatsapp_service.close_session()
        
        logger.info(f"Processed {responses_processed} WhatsApp responses")
        return responses_processed
        
    except Exception as e:
        logger.error(f"Error processing WhatsApp responses: {e}")
        return 0

@shared_task
def process_approval_response(message_id, response_text):
    """
    Process user approval/denial response.
    """
    try:
        message = WhatsAppMessage.objects.get(id=message_id)
        notification = message.notification
        
        # Use AI to analyze response if available
        ai_bot = AIBotConfiguration.objects.filter(
            purpose='response_processing',
            is_active=True
        ).first()
        
        if ai_bot:
            ai_service = AIBotService()
            analysis = ai_service.analyze_user_response(response_text, ai_bot)
            intent = analysis.get('intent', 'unclear')
        else:
            # Simple keyword matching
            response_lower = response_text.lower()
            if any(word in response_lower for word in ['approve', 'yes', 'ok', 'accept']):
                intent = 'approve'
            elif any(word in response_lower for word in ['deny', 'no', 'reject', 'cancel']):
                intent = 'deny'
            else:
                intent = 'unclear'
        
        # Update booking based on response
        if hasattr(notification, 'metadata') and 'booking_id' in notification.metadata:
            from bookings.models import Booking
            
            try:
                booking = Booking.objects.get(booking_id=notification.metadata['booking_id'])
                
                if intent == 'approve':
                    booking.status = 'confirmed'
                    # Trigger locker assignment and delivery process
                    assign_locker_and_notify.delay(booking.booking_id)
                    
                elif intent == 'deny':
                    booking.status = 'cancelled'
                    # Notify delivery agent and sender
                    notify_delivery_cancellation.delay(booking.booking_id)
                
                booking.save()
                
                # Send confirmation message
                send_confirmation_message.delay(message.recipient_phone, intent, booking.booking_id)
                
            except Booking.DoesNotExist:
                logger.error(f"Booking not found for notification {notification.notification_id}")
        
        logger.info(f"Processed approval response: {intent} for message {message_id}")
        
    except Exception as e:
        logger.error(f"Error processing approval response for message {message_id}: {e}")

@shared_task
def send_confirmation_message(phone_number, intent, booking_id):
    """
    Send confirmation message after processing approval response.
    """
    try:
        whatsapp_service = WhatsAppAutomationService()
        session = WhatsAppSession.objects.filter(status='active').first()
        
        if not session:
            return
        
        whatsapp_service.session = session
        whatsapp_service.initialize_driver(headless=True)
        
        if intent == 'approve':
            message = f"""✅ *Delivery Approved*

Thank you for approving the delivery!

Your parcel will be delivered to the assigned locker shortly. You'll receive another notification with the locker details and access code.

Booking ID: {booking_id}

Smart Locker Team"""
        
        elif intent == 'deny':
            message = f"""❌ *Delivery Cancelled*

Your delivery has been cancelled as requested.

The sender and delivery agent have been notified. If this was a mistake, please contact our support team.

Booking ID: {booking_id}

Smart Locker Team"""
        
        else:
            message = f"""❓ *Response Unclear*

We couldn't understand your response. Please reply with:
✅ *APPROVE* - to accept delivery
❌ *DENY* - to reject delivery

Booking ID: {booking_id}

Smart Locker Team"""
        
        whatsapp_service.send_message(phone_number, message)
        whatsapp_service.close_session()
        
    except Exception as e:
        logger.error(f"Error sending confirmation message: {e}")

@shared_task
def assign_locker_and_notify(booking_id):
    """
    Assign locker to approved booking and notify all parties.
    """
    try:
        from bookings.models import Booking
        from lockers.models import Locker
        
        booking = Booking.objects.get(booking_id=booking_id)
        
        # Find available locker
        available_locker = Locker.objects.filter(
            status='available',
            locker_type='standard'  # Can be enhanced with size/type matching
        ).first()
        
        if available_locker:
            # Assign locker
            booking.locker = available_locker
            available_locker.status = 'reserved'
            available_locker.save()
            booking.save()
            
            # Generate access code
            from lockers.models import LockerAccess
            import secrets
            
            access_code = secrets.token_hex(4).upper()
            
            LockerAccess.objects.create(
                locker=available_locker,
                access_code=access_code,
                access_type='qr_code',
                expires_at=timezone.now() + timedelta(hours=24),
                created_by=booking.customer
            )
            
            # Notify customer
            notify_locker_assignment.delay(booking.booking_id, access_code)
            
            # Notify delivery agent
            notify_delivery_agent.delay(booking.booking_id)
            
        else:
            logger.error(f"No available locker for booking {booking_id}")
            # Could implement waiting list or alternative handling
            
    except Exception as e:
        logger.error(f"Error assigning locker for booking {booking_id}: {e}")

@shared_task
def notify_locker_assignment(booking_id, access_code):
    """
    Notify customer about locker assignment.
    """
    try:
        from bookings.models import Booking
        
        booking = Booking.objects.get(booking_id=booking_id)
        
        message = f"""🔐 *Locker Assigned*

Your parcel delivery has been confirmed!

📍 *Locker Details:*
• Location: {booking.locker.locker_bank.location_description}
• Locker: {booking.locker}
• Access Code: *{access_code}*

⏰ *Collection:*
• Available: Now
• Expires: 24 hours

Instructions:
1. Go to the locker location
2. Enter access code on the kiosk
3. Collect your parcel

Smart Locker Team"""
        
        whatsapp_service = WhatsAppAutomationService()
        session = WhatsAppSession.objects.filter(status='active').first()
        
        if session:
            whatsapp_service.session = session
            whatsapp_service.initialize_driver(headless=True)
            whatsapp_service.send_message(booking.recipient_phone, message)
            whatsapp_service.close_session()
            
    except Exception as e:
        logger.error(f"Error notifying locker assignment for booking {booking_id}: {e}")

@shared_task
def notify_delivery_agent(booking_id):
    """
    Notify delivery agent about approved delivery.
    """
    try:
        from bookings.models import Booking
        
        booking = Booking.objects.get(booking_id=booking_id)
        
        if booking.delivery_agent:
            message = f"""📦 *Delivery Approved*

The customer has approved the delivery!

📋 *Details:*
• Booking: {booking.booking_id}
• Customer: {booking.recipient_name}
• Locker: {booking.locker}
• Location: {booking.locker.locker_bank.location_description}

Please proceed with the delivery to the assigned locker.

Smart Locker Team"""
            
            # Send notification to delivery agent
            # This could be via WhatsApp, push notification, or in-app notification
            
    except Exception as e:
        logger.error(f"Error notifying delivery agent for booking {booking_id}: {e}")

@shared_task
def notify_delivery_cancellation(booking_id):
    """
    Notify relevant parties about delivery cancellation.
    """
    try:
        from bookings.models import Booking
        
        booking = Booking.objects.get(booking_id=booking_id)
        
        # Notify delivery agent
        if booking.delivery_agent:
            agent_message = f"""❌ *Delivery Cancelled*

The customer has cancelled the delivery.

📋 *Details:*
• Booking: {booking.booking_id}
• Customer: {booking.recipient_name}
• Item: {booking.item_description}

Please do not proceed with this delivery.

Smart Locker Team"""
            
            # Send to delivery agent (implementation depends on preferred channel)
        
        # Notify sender if different from customer
        if booking.sender_phone != booking.recipient_phone:
            sender_message = f"""❌ *Delivery Cancelled*

The recipient has cancelled the delivery for booking {booking.booking_id}.

Please contact the recipient directly if needed.

Smart Locker Team"""
            
            # Send to sender
            
    except Exception as e:
        logger.error(f"Error notifying delivery cancellation for booking {booking_id}: {e}")

@shared_task
def cleanup_expired_sessions():
    """
    Clean up expired WhatsApp sessions and OTP verifications.
    """
    try:
        # Clean up expired WhatsApp sessions
        expired_sessions = WhatsAppSession.objects.filter(
            last_activity__lt=timezone.now() - timedelta(hours=2),
            status='active'
        )
        
        for session in expired_sessions:
            session.status = 'expired'
            session.save()
        
        # Clean up expired OTP verifications
        expired_otps = OTPVerification.objects.filter(
            expires_at__lt=timezone.now(),
            status__in=['generated', 'sent']
        )
        
        expired_otps.update(status='expired')
        
        logger.info(f"Cleaned up {expired_sessions.count()} sessions and {expired_otps.count()} OTPs")
        
    except Exception as e:
        logger.error(f"Error cleaning up expired sessions: {e}")

@shared_task
def generate_ai_otp(user_id, otp_type, phone_number):
    """
    Generate OTP using AI service.
    """
    try:
        from accounts.models import User
        
        user = User.objects.get(id=user_id)
        
        # Get AI bot configuration for OTP generation
        ai_bot = AIBotConfiguration.objects.filter(
            purpose='otp_generation',
            is_active=True
        ).first()
        
        ai_service = AIBotService()
        
        if ai_bot and ai_bot.provider == 'openai':
            ai_service.initialize_openai(ai_bot.api_key)
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
        send_otp_whatsapp.delay(otp_verification.id)
        
        return otp_code
        
    except Exception as e:
        logger.error(f"Error generating AI OTP: {e}")
        return None

@shared_task
def send_otp_whatsapp(otp_verification_id):
    """
    Send OTP via WhatsApp.
    """
    try:
        otp_verification = OTPVerification.objects.get(id=otp_verification_id)
        
        whatsapp_service = WhatsAppAutomationService()
        session = WhatsAppSession.objects.filter(status='active').first()
        
        if not session:
            logger.error("No active WhatsApp session for OTP sending")
            return False
        
        whatsapp_service.session = session
        whatsapp_service.initialize_driver(headless=True)
        
        success = whatsapp_service.send_otp_message(
            otp_verification.phone_number,
            otp_verification.otp_code,
            otp_verification.otp_type
        )
        
        if success:
            otp_verification.status = 'sent'
            otp_verification.sent_at = timezone.now()
        else:
            otp_verification.status = 'failed'
        
        otp_verification.save()
        whatsapp_service.close_session()
        
        return success
        
    except Exception as e:
        logger.error(f"Error sending OTP via WhatsApp: {e}")
        return False