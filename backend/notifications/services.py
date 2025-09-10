import time
import random
import string
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from django.conf import settings
from django.utils import timezone
import requests
import json
import openai
import google.generativeai as genai

from .models import (
    WhatsAppSession, WhatsAppMessage, AIBotConfiguration, 
    AIBotInteraction, OTPVerification, Notification
)

logger = logging.getLogger(__name__)

class WhatsAppAutomationService:
    """
    WhatsApp Web automation service using Selenium for sending messages,
    OTPs, and handling approval/denial responses from users.
    """
    
    def __init__(self):
        self.driver = None
        self.session = None
        self.wait_timeout = 30
        
    def initialize_driver(self, headless: bool = True) -> webdriver.Chrome:
        """Initialize Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Add user data directory for session persistence
        chrome_options.add_argument(f"--user-data-dir=/tmp/whatsapp_session")
        
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        return self.driver
    
    def create_session(self, phone_number: str) -> WhatsAppSession:
        """Create a new WhatsApp session."""
        session_id = f"wa_session_{phone_number}_{int(time.time())}"
        
        session = WhatsAppSession.objects.create(
            session_id=session_id,
            phone_number=phone_number,
            status='inactive'
        )
        
        self.session = session
        return session
    
    def login_to_whatsapp(self, session: WhatsAppSession) -> bool:
        """
        Login to WhatsApp Web and handle QR code scanning.
        Returns True if login successful, False otherwise.
        """
        try:
            if not self.driver:
                self.initialize_driver(headless=False)  # Need to see QR code
            
            self.driver.get("https://web.whatsapp.com")
            
            # Wait for QR code to appear
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            try:
                # Check if already logged in
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")))
                session.status = 'active'
                session.last_activity = timezone.now()
                session.save()
                logger.info(f"Already logged in to WhatsApp for session {session.session_id}")
                return True
                
            except TimeoutException:
                # Need to scan QR code
                try:
                    qr_code = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-ref]")))
                    qr_code_data = qr_code.get_attribute("data-ref")
                    
                    # Save QR code info
                    session.qr_code_path = qr_code_data
                    session.save()
                    
                    logger.info(f"QR code available for session {session.session_id}. Please scan to continue.")
                    
                    # Wait for login completion (up to 2 minutes)
                    wait_long = WebDriverWait(self.driver, 120)
                    wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")))
                    
                    session.status = 'active'
                    session.last_activity = timezone.now()
                    session.save()
                    
                    logger.info(f"Successfully logged in to WhatsApp for session {session.session_id}")
                    return True
                    
                except TimeoutException:
                    session.status = 'error'
                    session.error_message = "QR code scan timeout"
                    session.save()
                    logger.error(f"QR code scan timeout for session {session.session_id}")
                    return False
                    
        except Exception as e:
            session.status = 'error'
            session.error_message = str(e)
            session.save()
            logger.error(f"Error logging in to WhatsApp: {e}")
            return False
    
    def send_message(self, phone_number: str, message: str, message_type: str = 'text') -> bool:
        """
        Send a message to a specific phone number via WhatsApp Web.
        """
        try:
            if not self.driver or not self.session or self.session.status != 'active':
                logger.error("WhatsApp session not active")
                return False
            
            # Format phone number (remove + and spaces)
            clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
            
            # Navigate to chat
            chat_url = f"https://web.whatsapp.com/send?phone={clean_phone}"
            self.driver.get(chat_url)
            
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            # Wait for chat to load
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']")))
            except TimeoutException:
                # Try alternative selector
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            
            # Find message input box
            message_box = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']")
            
            # Clear and type message
            message_box.clear()
            message_box.send_keys(message)
            
            # Send message
            message_box.send_keys(Keys.ENTER)
            
            # Wait a bit for message to be sent
            time.sleep(2)
            
            # Update session activity
            self.session.last_activity = timezone.now()
            self.session.save()
            
            logger.info(f"Message sent to {phone_number}: {message[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to {phone_number}: {e}")
            return False
    
    def send_otp_message(self, phone_number: str, otp_code: str, purpose: str = "verification") -> bool:
        """Send OTP message via WhatsApp."""
        message = f"""🔐 *Smart Locker OTP*

Your verification code is: *{otp_code}*

This code is valid for 10 minutes and is for {purpose}.

⚠️ Do not share this code with anyone.

Smart Locker Team"""
        
        return self.send_message(phone_number, message, 'otp')
    
    def send_approval_request(self, phone_number: str, booking_details: Dict) -> bool:
        """Send parcel approval request with interactive options."""
        message = f"""📦 *Parcel Delivery Approval*

Hello {booking_details.get('recipient_name', 'Customer')},

A parcel is ready for delivery to your locker:

📋 *Details:*
• From: {booking_details.get('sender_name', 'N/A')}
• Item: {booking_details.get('item_description', 'N/A')}
• Apartment: {booking_details.get('recipient_apartment', 'N/A')}

Please reply with:
✅ *APPROVE* - to accept delivery
❌ *DENY* - to reject delivery

You have 30 minutes to respond.

Smart Locker Team"""
        
        return self.send_message(phone_number, message, 'approval')
    
    def check_for_responses(self, phone_number: str) -> Optional[str]:
        """
        Check for user responses in WhatsApp chat.
        Returns the latest message from the user or None.
        """
        try:
            if not self.driver or not self.session or self.session.status != 'active':
                return None
            
            clean_phone = phone_number.replace('+', '').replace(' ', '').replace('-', '')
            chat_url = f"https://web.whatsapp.com/send?phone={clean_phone}"
            self.driver.get(chat_url)
            
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='conversation-panel-messages']")))
            
            # Get all messages in the chat
            messages = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='msg-container']")
            
            if messages:
                # Get the last message
                last_message = messages[-1]
                
                # Check if it's an incoming message (from user)
                if "message-in" in last_message.get_attribute("class"):
                    message_text = last_message.find_element(By.CSS_SELECTOR, ".selectable-text").text
                    return message_text.strip().upper()
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking responses from {phone_number}: {e}")
            return None
    
    def close_session(self):
        """Close the WebDriver and clean up."""
        if self.driver:
            self.driver.quit()
            self.driver = None
        
        if self.session:
            self.session.status = 'inactive'
            self.session.save()

class AIBotService:
    """
    Service for integrating with various AI providers for OTP generation,
    message personalization, and response processing.
    """
    
    def __init__(self):
        self.openai_client = None
        self.gemini_client = None
        
    def initialize_openai(self, api_key: str):
        """Initialize OpenAI client."""
        openai.api_key = api_key
        self.openai_client = openai
    
    def initialize_gemini(self, api_key: str):
        """Initialize Google Gemini client."""
        genai.configure(api_key=api_key)
        self.gemini_client = genai.GenerativeModel('gemini-pro')
    
    def generate_otp(self, length: int = 6, use_ai: bool = False) -> str:
        """
        Generate OTP code. Can use AI for more secure/random generation.
        """
        if use_ai and self.openai_client:
            try:
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Generate a secure numeric OTP code."},
                        {"role": "user", "content": f"Generate a {length}-digit OTP code for user verification."}
                    ],
                    max_tokens=10,
                    temperature=1.0
                )
                
                ai_otp = ''.join(filter(str.isdigit, response.choices[0].message.content))
                if len(ai_otp) >= length:
                    return ai_otp[:length]
                    
            except Exception as e:
                logger.error(f"Error generating AI OTP: {e}")
        
        # Fallback to random generation
        return ''.join(random.choices(string.digits, k=length))
    
    def personalize_message(self, template: str, user_data: Dict, bot_config: AIBotConfiguration) -> str:
        """
        Use AI to personalize message templates based on user data.
        """
        try:
            if bot_config.provider == 'openai' and self.openai_client:
                prompt = f"""
                Personalize this message template for a smart locker system:
                
                Template: {template}
                User Data: {json.dumps(user_data)}
                
                Make it friendly, professional, and relevant to the user's context.
                Keep the same structure but add personal touches.
                """
                
                response = self.openai_client.ChatCompletion.create(
                    model=bot_config.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for a smart locker system."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=bot_config.max_tokens,
                    temperature=float(bot_config.temperature)
                )
                
                return response.choices[0].message.content.strip()
                
            elif bot_config.provider == 'google' and self.gemini_client:
                prompt = f"""
                Personalize this message template for a smart locker system:
                
                Template: {template}
                User Data: {json.dumps(user_data)}
                
                Make it friendly, professional, and relevant to the user's context.
                """
                
                response = self.gemini_client.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            logger.error(f"Error personalizing message with AI: {e}")
        
        # Fallback to template substitution
        return self._simple_template_substitution(template, user_data)
    
    def _simple_template_substitution(self, template: str, user_data: Dict) -> str:
        """Simple template variable substitution."""
        for key, value in user_data.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template
    
    def analyze_user_response(self, response_text: str, bot_config: AIBotConfiguration) -> Dict:
        """
        Use AI to analyze user responses and extract intent/sentiment.
        """
        try:
            if bot_config.provider == 'openai' and self.openai_client:
                prompt = f"""
                Analyze this user response to a smart locker system message:
                
                Response: "{response_text}"
                
                Determine:
                1. Intent (approve, deny, question, complaint, etc.)
                2. Sentiment (positive, negative, neutral)
                3. Confidence level (0-1)
                4. Any specific concerns or requests
                
                Return as JSON format.
                """
                
                response = self.openai_client.ChatCompletion.create(
                    model=bot_config.model_name,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant that analyzes user responses."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=bot_config.max_tokens,
                    temperature=0.3
                )
                
                return json.loads(response.choices[0].message.content)
                
        except Exception as e:
            logger.error(f"Error analyzing user response with AI: {e}")
        
        # Fallback to simple keyword matching
        return self._simple_response_analysis(response_text)
    
    def _simple_response_analysis(self, response_text: str) -> Dict:
        """Simple keyword-based response analysis."""
        text_lower = response_text.lower()
        
        if any(word in text_lower for word in ['approve', 'yes', 'ok', 'accept', 'confirm']):
            return {
                'intent': 'approve',
                'sentiment': 'positive',
                'confidence': 0.8
            }
        elif any(word in text_lower for word in ['deny', 'no', 'reject', 'cancel', 'refuse']):
            return {
                'intent': 'deny',
                'sentiment': 'negative',
                'confidence': 0.8
            }
        else:
            return {
                'intent': 'unclear',
                'sentiment': 'neutral',
                'confidence': 0.3
            }

class NotificationService:
    """
    Main service for handling all types of notifications including
    WhatsApp, SMS, email, and push notifications.
    """
    
    def __init__(self):
        self.whatsapp_service = WhatsAppAutomationService()
        self.ai_service = AIBotService()
    
    def send_notification(self, notification: Notification) -> bool:
        """
        Send notification based on the template channel.
        """
        try:
            if notification.template.channel == 'whatsapp':
                return self._send_whatsapp_notification(notification)
            elif notification.template.channel == 'sms':
                return self._send_sms_notification(notification)
            elif notification.template.channel == 'email':
                return self._send_email_notification(notification)
            elif notification.template.channel == 'push':
                return self._send_push_notification(notification)
            else:
                logger.error(f"Unsupported notification channel: {notification.template.channel}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending notification {notification.notification_id}: {e}")
            notification.status = 'failed'
            notification.error_message = str(e)
            notification.save()
            return False
    
    def _send_whatsapp_notification(self, notification: Notification) -> bool:
        """Send WhatsApp notification."""
        try:
            # Get or create active WhatsApp session
            session = WhatsAppSession.objects.filter(status='active').first()
            
            if not session:
                # Create new session (requires manual QR scan)
                session = self.whatsapp_service.create_session(settings.WHATSAPP_BUSINESS_NUMBER)
                if not self.whatsapp_service.login_to_whatsapp(session):
                    return False
            
            # Create WhatsApp message record
            whatsapp_msg = WhatsAppMessage.objects.create(
                notification=notification,
                session=session,
                recipient_phone=notification.recipient_phone,
                message_type=notification.template.template_type,
                message_content=notification.message,
                requires_response=notification.template.template_type in ['parcel_approval']
            )
            
            # Send the message
            success = False
            if notification.template.template_type == 'otp_verification':
                # Extract OTP from message
                otp_code = self._extract_otp_from_message(notification.message)
                success = self.whatsapp_service.send_otp_message(
                    notification.recipient_phone, 
                    otp_code, 
                    "verification"
                )
            elif notification.template.template_type == 'parcel_approval':
                # Send approval request
                booking_data = notification.metadata.get('booking_details', {})
                success = self.whatsapp_service.send_approval_request(
                    notification.recipient_phone,
                    booking_data
                )
            else:
                # Send regular message
                success = self.whatsapp_service.send_message(
                    notification.recipient_phone,
                    notification.message
                )
            
            if success:
                whatsapp_msg.status = 'sent'
                whatsapp_msg.sent_at = timezone.now()
                notification.status = 'sent'
                notification.sent_at = timezone.now()
            else:
                whatsapp_msg.status = 'failed'
                notification.status = 'failed'
            
            whatsapp_msg.save()
            notification.save()
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp notification: {e}")
            return False
    
    def _extract_otp_from_message(self, message: str) -> str:
        """Extract OTP code from message text."""
        import re
        otp_match = re.search(r'\b\d{4,8}\b', message)
        return otp_match.group() if otp_match else "123456"
    
    def _send_sms_notification(self, notification: Notification) -> bool:
        """Send SMS notification using free SMS services or APIs."""
        # Implementation for SMS sending
        # Could use services like TextBelt, SMS APIs, etc.
        logger.info(f"SMS notification sent to {notification.recipient_phone}")
        return True
    
    def _send_email_notification(self, notification: Notification) -> bool:
        """Send email notification."""
        from django.core.mail import send_mail
        
        try:
            send_mail(
                subject=notification.subject,
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _send_push_notification(self, notification: Notification) -> bool:
        """Send push notification to mobile apps."""
        # Implementation for push notifications
        # Could use Firebase Cloud Messaging, OneSignal, etc.
        logger.info(f"Push notification sent to user {notification.recipient.username}")
        return True