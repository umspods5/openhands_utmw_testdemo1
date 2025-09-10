from django.core.management.base import BaseCommand
from django.conf import settings
from notifications.services import WhatsAppAutomationService
from notifications.models import WhatsAppSession, AIBotConfiguration
import os


class Command(BaseCommand):
    help = 'Set up WhatsApp Web session for automated messaging'

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Business WhatsApp phone number (with country code)',
            default='+919876543210'
        )
        parser.add_argument(
            '--headless',
            action='store_true',
            help='Run in headless mode (no GUI)',
        )
        parser.add_argument(
            '--setup-ai',
            action='store_true',
            help='Also set up AI bot configurations',
        )

    def handle(self, *args, **options):
        phone_number = options['phone']
        headless = options['headless']
        setup_ai = options['setup_ai']

        self.stdout.write(
            self.style.SUCCESS(f'Setting up WhatsApp session for {phone_number}')
        )

        # Initialize WhatsApp service
        whatsapp_service = WhatsAppAutomationService()
        
        # Create session
        session = whatsapp_service.create_session(phone_number)
        
        self.stdout.write(f'Created session: {session.session_id}')
        
        # Initialize driver
        whatsapp_service.initialize_driver(headless=headless)
        
        if not headless:
            self.stdout.write(
                self.style.WARNING(
                    'Browser window opened. Please scan the QR code with your WhatsApp mobile app.'
                )
            )
        
        # Attempt login
        success = whatsapp_service.login_to_whatsapp(session)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS('✅ WhatsApp session established successfully!')
            )
            
            # Test message
            test_message = "🤖 Smart Locker WhatsApp automation is now active!"
            if whatsapp_service.send_message(phone_number, test_message):
                self.stdout.write(
                    self.style.SUCCESS('✅ Test message sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Failed to send test message')
                )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to establish WhatsApp session')
            )
        
        # Set up AI configurations if requested
        if setup_ai:
            self.setup_ai_bots()
        
        # Close session
        whatsapp_service.close_session()

    def setup_ai_bots(self):
        """Set up AI bot configurations for different purposes."""
        self.stdout.write('Setting up AI bot configurations...')
        
        # OpenAI GPT for customer support
        openai_config, created = AIBotConfiguration.objects.get_or_create(
            name='OpenAI Customer Support',
            provider='openai',
            purpose='customer_support',
            defaults={
                'model_name': 'gpt-3.5-turbo',
                'max_tokens': 150,
                'temperature': 0.7,
                'daily_limit': 1000,
                'monthly_limit': 30000,
                'api_key': os.getenv('OPENAI_API_KEY', ''),
            }
        )
        
        if created:
            self.stdout.write('✅ Created OpenAI customer support bot')
        
        # Google Gemini for message personalization
        gemini_config, created = AIBotConfiguration.objects.get_or_create(
            name='Gemini Message Personalizer',
            provider='google',
            purpose='message_personalization',
            defaults={
                'model_name': 'gemini-pro',
                'max_tokens': 200,
                'temperature': 0.8,
                'daily_limit': 1500,
                'monthly_limit': 45000,
                'api_key': os.getenv('GOOGLE_API_KEY', ''),
            }
        )
        
        if created:
            self.stdout.write('✅ Created Gemini message personalizer bot')
        
        # OpenAI for response processing
        response_config, created = AIBotConfiguration.objects.get_or_create(
            name='OpenAI Response Processor',
            provider='openai',
            purpose='response_processing',
            defaults={
                'model_name': 'gpt-3.5-turbo',
                'max_tokens': 100,
                'temperature': 0.3,
                'daily_limit': 2000,
                'monthly_limit': 60000,
                'api_key': os.getenv('OPENAI_API_KEY', ''),
            }
        )
        
        if created:
            self.stdout.write('✅ Created OpenAI response processor bot')
        
        # OTP generation bot
        otp_config, created = AIBotConfiguration.objects.get_or_create(
            name='AI OTP Generator',
            provider='openai',
            purpose='otp_generation',
            defaults={
                'model_name': 'gpt-3.5-turbo',
                'max_tokens': 10,
                'temperature': 1.0,
                'daily_limit': 500,
                'monthly_limit': 15000,
                'api_key': os.getenv('OPENAI_API_KEY', ''),
            }
        )
        
        if created:
            self.stdout.write('✅ Created AI OTP generator bot')
        
        self.stdout.write(
            self.style.SUCCESS('🤖 AI bot configurations completed!')
        )
        
        # Display API key status
        if not os.getenv('OPENAI_API_KEY'):
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  OPENAI_API_KEY not set. Please add it to your environment variables.'
                )
            )
        
        if not os.getenv('GOOGLE_API_KEY'):
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  GOOGLE_API_KEY not set. Please add it to your environment variables.'
                )
            )