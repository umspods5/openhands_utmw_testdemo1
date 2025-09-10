from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notifications.services import WhatsAppAutomationService, AIBotService
from notifications.models import WhatsAppSession, AIBotConfiguration, OTPVerification
from notifications.tasks import generate_ai_otp, send_otp_whatsapp
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Test WhatsApp messaging functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            required=True,
            help='Recipient phone number (with country code)',
        )
        parser.add_argument(
            '--test-type',
            type=str,
            choices=['otp', 'approval', 'message', 'all'],
            default='message',
            help='Type of test to run',
        )
        parser.add_argument(
            '--message',
            type=str,
            help='Custom message to send',
            default='Hello from Smart Locker system! 🤖'
        )

    def handle(self, *args, **options):
        phone_number = options['phone']
        test_type = options['test_type']
        custom_message = options['message']

        self.stdout.write(
            self.style.SUCCESS(f'Testing WhatsApp messaging to {phone_number}')
        )

        # Check for active session
        session = WhatsAppSession.objects.filter(status='active').first()
        if not session:
            self.stdout.write(
                self.style.ERROR(
                    '❌ No active WhatsApp session found. Run "python manage.py setup_whatsapp" first.'
                )
            )
            return

        # Initialize service
        whatsapp_service = WhatsAppAutomationService()
        whatsapp_service.session = session
        whatsapp_service.initialize_driver(headless=True)

        if test_type == 'message' or test_type == 'all':
            self.test_simple_message(whatsapp_service, phone_number, custom_message)

        if test_type == 'otp' or test_type == 'all':
            self.test_otp_message(whatsapp_service, phone_number)

        if test_type == 'approval' or test_type == 'all':
            self.test_approval_message(whatsapp_service, phone_number)

        # Close session
        whatsapp_service.close_session()

    def test_simple_message(self, service, phone_number, message):
        """Test sending a simple text message."""
        self.stdout.write('📱 Testing simple message...')
        
        success = service.send_message(phone_number, message)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS('✅ Simple message sent successfully!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to send simple message')
            )

    def test_otp_message(self, service, phone_number):
        """Test sending OTP message."""
        self.stdout.write('🔐 Testing OTP message...')
        
        # Generate random OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        success = service.send_otp_message(phone_number, otp_code, "testing")
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'✅ OTP message sent successfully! Code: {otp_code}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to send OTP message')
            )

    def test_approval_message(self, service, phone_number):
        """Test sending approval request message."""
        self.stdout.write('📦 Testing approval request message...')
        
        # Mock booking details
        booking_details = {
            'recipient_name': 'John Doe',
            'sender_name': 'Amazon Delivery',
            'item_description': 'Electronics Package',
            'recipient_apartment': 'Apt 101, Building A'
        }
        
        success = service.send_approval_request(phone_number, booking_details)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS('✅ Approval request sent successfully!')
            )
            
            # Test response checking
            self.stdout.write('Checking for responses in 10 seconds...')
            import time
            time.sleep(10)
            
            response = service.check_for_responses(phone_number)
            if response:
                self.stdout.write(
                    self.style.SUCCESS(f'📨 Received response: "{response}"')
                )
                
                # Analyze response with AI if available
                ai_bot = AIBotConfiguration.objects.filter(
                    purpose='response_processing',
                    is_active=True
                ).first()
                
                if ai_bot:
                    ai_service = AIBotService()
                    analysis = ai_service.analyze_user_response(response, ai_bot)
                    self.stdout.write(f'🤖 AI Analysis: {analysis}')
                
            else:
                self.stdout.write('📭 No response received yet')
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to send approval request')
            )

    def test_ai_otp_generation(self, phone_number):
        """Test AI-powered OTP generation."""
        self.stdout.write('🤖 Testing AI OTP generation...')
        
        # Get or create test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'phone_number': phone_number
            }
        )
        
        if created:
            self.stdout.write('Created test user')
        
        # Generate AI OTP
        otp_code = generate_ai_otp.delay(user.id, 'testing', phone_number)
        
        if otp_code:
            self.stdout.write(
                self.style.SUCCESS(f'✅ AI OTP generated: {otp_code}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to generate AI OTP')
            )