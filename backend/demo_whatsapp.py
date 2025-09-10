#!/usr/bin/env python
"""
Demo script for WhatsApp Automation System
This script demonstrates the key features of the WhatsApp automation system.
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartlocker.settings')
django.setup()

from django.contrib.auth import get_user_model
from notifications.utils import (
    WhatsAppMessenger, OTPManager, SmartNotificationManager,
    send_whatsapp_message, send_otp_to_user, verify_user_otp
)
from notifications.models import AIBotConfiguration, WhatsAppSession

User = get_user_model()

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n🔹 Step {step}: {description}")

def check_system_status():
    """Check if the WhatsApp system is ready."""
    print_header("SYSTEM STATUS CHECK")
    
    # Check for active WhatsApp session
    active_sessions = WhatsAppSession.objects.filter(status='active').count()
    print(f"📱 Active WhatsApp Sessions: {active_sessions}")
    
    # Check AI bot configurations
    ai_bots = AIBotConfiguration.objects.filter(is_active=True).count()
    print(f"🤖 Active AI Bots: {ai_bots}")
    
    if active_sessions == 0:
        print("\n⚠️  WARNING: No active WhatsApp sessions found!")
        print("   Run: python manage.py setup_whatsapp --phone +919876543210")
        return False
    
    print("\n✅ System is ready for WhatsApp automation!")
    return True

def demo_simple_messaging():
    """Demonstrate simple WhatsApp messaging."""
    print_header("SIMPLE WHATSAPP MESSAGING")
    
    phone_number = input("Enter phone number (with country code, e.g., +919876543210): ")
    if not phone_number:
        phone_number = "+919876543210"  # Default for demo
    
    print_step(1, "Sending a simple WhatsApp message")
    
    message = f"""🤖 *Smart Locker Demo*

Hello! This is a demonstration of our WhatsApp automation system.

✅ Features:
• Automated messaging
• OTP verification
• Parcel approval requests
• AI-powered responses

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Smart Locker Team"""
    
    success = send_whatsapp_message(phone_number, message)
    
    if success:
        print("✅ Message sent successfully!")
    else:
        print("❌ Failed to send message")
    
    return success

def demo_otp_system():
    """Demonstrate OTP system."""
    print_header("OTP VERIFICATION SYSTEM")
    
    # Get or create demo user
    username = input("Enter username for demo (or press Enter for 'demo_user'): ")
    if not username:
        username = "demo_user"
    
    phone_number = input("Enter phone number (or press Enter for +919876543210): ")
    if not phone_number:
        phone_number = "+919876543210"
    
    print_step(1, f"Creating/getting user: {username}")
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@example.com',
            'phone_number': phone_number
        }
    )
    
    if created:
        print(f"✅ Created new user: {username}")
    else:
        print(f"✅ Using existing user: {username}")
    
    print_step(2, "Generating and sending OTP via WhatsApp")
    
    otp_code = send_otp_to_user(user, phone_number, "demo")
    
    if otp_code:
        print(f"✅ OTP sent successfully!")
        print(f"📱 OTP Code: {otp_code} (for demo purposes)")
        
        # Demo verification
        print_step(3, "Verifying OTP")
        verify_code = input(f"Enter the OTP code (or press Enter to use {otp_code}): ")
        if not verify_code:
            verify_code = otp_code
        
        is_valid = verify_user_otp(user, verify_code, "demo")
        
        if is_valid:
            print("✅ OTP verified successfully!")
        else:
            print("❌ OTP verification failed")
        
        return is_valid
    else:
        print("❌ Failed to send OTP")
        return False

def demo_approval_system():
    """Demonstrate parcel approval system."""
    print_header("PARCEL APPROVAL SYSTEM")
    
    phone_number = input("Enter phone number for approval demo: ")
    if not phone_number:
        phone_number = "+919876543210"
    
    print_step(1, "Sending parcel approval request")
    
    # Create demo booking details
    booking_details = {
        'recipient_name': 'John Doe',
        'sender_name': 'Amazon Delivery',
        'item_description': 'Electronics Package (Demo)',
        'recipient_apartment': 'Apt 101, Building A'
    }
    
    messenger = WhatsAppMessenger()
    success = messenger.send_parcel_approval_request(phone_number, booking_details)
    
    if success:
        print("✅ Approval request sent successfully!")
        print("📱 User will receive an interactive message with APPROVE/DENY options")
        
        print_step(2, "Checking for user response")
        print("⏳ Waiting 15 seconds for user response...")
        
        import time
        time.sleep(15)
        
        response = messenger.check_user_response(phone_number)
        
        if response:
            print(f"📨 User response received: '{response}'")
            
            # Analyze response
            if any(word in response.lower() for word in ['approve', 'yes', 'ok', 'accept']):
                print("✅ User APPROVED the delivery!")
            elif any(word in response.lower() for word in ['deny', 'no', 'reject', 'cancel']):
                print("❌ User DENIED the delivery!")
            else:
                print("❓ Response unclear, may need manual review")
        else:
            print("📭 No response received yet")
        
        return True
    else:
        print("❌ Failed to send approval request")
        return False

def demo_ai_personalization():
    """Demonstrate AI-powered message personalization."""
    print_header("AI-POWERED PERSONALIZATION")
    
    # Check if AI bots are configured
    ai_bots = AIBotConfiguration.objects.filter(is_active=True)
    
    if not ai_bots.exists():
        print("⚠️  No AI bots configured. Messages will use simple templates.")
        print("   To enable AI: Set OPENAI_API_KEY or GOOGLE_API_KEY in environment")
        return False
    
    print(f"🤖 Found {ai_bots.count()} active AI bot(s)")
    
    # Get demo user
    user = User.objects.filter(username='demo_user').first()
    if not user:
        print("❌ Demo user not found. Run OTP demo first.")
        return False
    
    print_step(1, "Sending AI-personalized notification")
    
    manager = SmartNotificationManager()
    
    context_data = {
        'booking_id': 'DEMO123456',
        'locker_number': 'L-A-001',
        'access_code': 'DEMO123',
        'item_description': 'Demo Package',
        'sender_name': 'Demo Sender'
    }
    
    success = manager.send_personalized_notification(
        user=user,
        template_type='delivery_update',
        channel='whatsapp',
        context_data=context_data,
        priority='high'
    )
    
    if success:
        print("✅ AI-personalized notification sent!")
        print("🧠 The message was customized based on user context and AI analysis")
    else:
        print("❌ Failed to send personalized notification")
    
    return success

def main():
    """Main demo function."""
    print_header("SMART LOCKER WHATSAPP AUTOMATION DEMO")
    print("This demo showcases the WhatsApp automation system features.")
    print("Make sure you have:")
    print("1. Set up WhatsApp session: python manage.py setup_whatsapp")
    print("2. Started Celery worker: celery -A smartlocker worker")
    print("3. Have a phone with WhatsApp for testing")
    
    if not check_system_status():
        print("\n❌ System not ready. Please set up WhatsApp session first.")
        return
    
    while True:
        print("\n" + "-"*60)
        print("DEMO OPTIONS:")
        print("1. Simple WhatsApp Messaging")
        print("2. OTP Verification System")
        print("3. Parcel Approval System")
        print("4. AI-Powered Personalization")
        print("5. System Status Check")
        print("0. Exit")
        print("-"*60)
        
        choice = input("Select demo option (0-5): ").strip()
        
        if choice == '0':
            print("\n👋 Demo completed. Thank you!")
            break
        elif choice == '1':
            demo_simple_messaging()
        elif choice == '2':
            demo_otp_system()
        elif choice == '3':
            demo_approval_system()
        elif choice == '4':
            demo_ai_personalization()
        elif choice == '5':
            check_system_status()
        else:
            print("❌ Invalid option. Please select 0-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the system setup and try again.")