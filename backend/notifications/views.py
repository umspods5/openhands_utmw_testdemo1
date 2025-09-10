from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging

from .models import (
    WhatsAppSession, WhatsAppMessage, OTPVerification, 
    AIBotConfiguration, Notification
)
from .utils import (
    WhatsAppMessenger, OTPManager, SmartNotificationManager,
    send_whatsapp_message, send_otp_to_user, verify_user_otp
)
from .tasks import process_whatsapp_responses
from .serializers import (
    WhatsAppSessionSerializer, WhatsAppMessageSerializer,
    OTPVerificationSerializer, NotificationSerializer
)

User = get_user_model()
logger = logging.getLogger(__name__)


class WhatsAppSessionView(APIView):
    """
    API view for managing WhatsApp sessions.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current WhatsApp session status."""
        sessions = WhatsAppSession.objects.all().order_by('-created_at')
        serializer = WhatsAppSessionSerializer(sessions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create new WhatsApp session."""
        phone_number = request.data.get('phone_number')
        
        if not phone_number:
            return Response(
                {'error': 'Phone number is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            messenger = WhatsAppMessenger()
            session = messenger.service.create_session(phone_number)
            
            serializer = WhatsAppSessionSerializer(session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error creating WhatsApp session: {e}")
            return Response(
                {'error': 'Failed to create session'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_whatsapp_message_api(request):
    """
    API endpoint to send WhatsApp message.
    """
    phone_number = request.data.get('phone_number')
    message = request.data.get('message')
    
    if not phone_number or not message:
        return Response(
            {'error': 'Phone number and message are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        success = send_whatsapp_message(phone_number, message)
        
        if success:
            return Response(
                {'success': True, 'message': 'Message sent successfully'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': False, 'error': 'Failed to send message'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_otp_api(request):
    """
    API endpoint to send OTP via WhatsApp.
    """
    phone_number = request.data.get('phone_number')
    user_id = request.data.get('user_id')
    otp_type = request.data.get('otp_type', 'verification')
    
    if not phone_number:
        return Response(
            {'error': 'Phone number is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get user
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            # Try to find user by phone number
            user = User.objects.filter(phone_number=phone_number).first()
            if not user:
                return Response(
                    {'error': 'User not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        otp_code = send_otp_to_user(user, phone_number, otp_type)
        
        if otp_code:
            return Response(
                {
                    'success': True, 
                    'message': 'OTP sent successfully',
                    'otp_code': otp_code  # Remove in production
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': False, 'error': 'Failed to send OTP'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error sending OTP: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_otp_api(request):
    """
    API endpoint to verify OTP.
    """
    user_id = request.data.get('user_id')
    otp_code = request.data.get('otp_code')
    otp_type = request.data.get('otp_type', 'verification')
    
    if not user_id or not otp_code:
        return Response(
            {'error': 'User ID and OTP code are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
        is_valid = verify_user_otp(user, otp_code, otp_type)
        
        if is_valid:
            return Response(
                {'success': True, 'message': 'OTP verified successfully'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': False, 'error': 'Invalid or expired OTP'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error verifying OTP: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_approval_request_api(request):
    """
    API endpoint to send parcel approval request.
    """
    phone_number = request.data.get('phone_number')
    booking_details = request.data.get('booking_details', {})
    
    if not phone_number:
        return Response(
            {'error': 'Phone number is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        messenger = WhatsAppMessenger()
        success = messenger.send_parcel_approval_request(phone_number, booking_details)
        
        if success:
            return Response(
                {'success': True, 'message': 'Approval request sent successfully'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': False, 'error': 'Failed to send approval request'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error sending approval request: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_responses_api(request):
    """
    API endpoint to check for WhatsApp responses.
    """
    phone_number = request.query_params.get('phone_number')
    
    if not phone_number:
        return Response(
            {'error': 'Phone number is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        messenger = WhatsAppMessenger()
        response = messenger.check_user_response(phone_number)
        
        return Response(
            {
                'phone_number': phone_number,
                'response': response,
                'has_response': bool(response)
            }, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error checking responses: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_responses_api(request):
    """
    API endpoint to trigger response processing.
    """
    try:
        # Trigger async task to process responses
        task = process_whatsapp_responses.delay()
        
        return Response(
            {
                'success': True, 
                'message': 'Response processing triggered',
                'task_id': task.id
            }, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error triggering response processing: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class WhatsAppMessageView(APIView):
    """
    API view for WhatsApp messages.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get WhatsApp messages."""
        messages = WhatsAppMessage.objects.all().order_by('-created_at')
        
        # Filter by phone number if provided
        phone_number = request.query_params.get('phone_number')
        if phone_number:
            messages = messages.filter(recipient_phone=phone_number)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            messages = messages.filter(status=status_filter)
        
        # Filter by message type if provided
        message_type = request.query_params.get('message_type')
        if message_type:
            messages = messages.filter(message_type=message_type)
        
        serializer = WhatsAppMessageSerializer(messages, many=True)
        return Response(serializer.data)


class OTPVerificationView(APIView):
    """
    API view for OTP verifications.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get OTP verifications."""
        otps = OTPVerification.objects.all().order_by('-created_at')
        
        # Filter by user if provided
        user_id = request.query_params.get('user_id')
        if user_id:
            otps = otps.filter(user_id=user_id)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            otps = otps.filter(status=status_filter)
        
        # Filter by OTP type if provided
        otp_type = request.query_params.get('otp_type')
        if otp_type:
            otps = otps.filter(otp_type=otp_type)
        
        serializer = OTPVerificationSerializer(otps, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_personalized_notification_api(request):
    """
    API endpoint to send personalized notification.
    """
    user_id = request.data.get('user_id')
    template_type = request.data.get('template_type')
    channel = request.data.get('channel', 'whatsapp')
    context_data = request.data.get('context_data', {})
    priority = request.data.get('priority', 'medium')
    
    if not user_id or not template_type:
        return Response(
            {'error': 'User ID and template type are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
        manager = SmartNotificationManager()
        
        success = manager.send_personalized_notification(
            user, template_type, channel, context_data, priority
        )
        
        if success:
            return Response(
                {'success': True, 'message': 'Notification sent successfully'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': False, 'error': 'Failed to send notification'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error sending personalized notification: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def whatsapp_status_api(request):
    """
    API endpoint to get WhatsApp system status.
    """
    try:
        # Get active sessions
        active_sessions = WhatsAppSession.objects.filter(status='active').count()
        
        # Get recent messages
        recent_messages = WhatsAppMessage.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        # Get pending approvals
        pending_approvals = WhatsAppMessage.objects.filter(
            message_type='approval',
            requires_response=True,
            user_response='',
            status='sent'
        ).count()
        
        # Get AI bot status
        ai_bots = AIBotConfiguration.objects.filter(is_active=True).count()
        
        return Response(
            {
                'active_sessions': active_sessions,
                'recent_messages_24h': recent_messages,
                'pending_approvals': pending_approvals,
                'active_ai_bots': ai_bots,
                'system_status': 'operational' if active_sessions > 0 else 'inactive'
            }, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error getting WhatsApp status: {e}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
