# WhatsApp Automation & AI Bot Integration Guide

## 🚀 Overview

This Smart Locker system includes a comprehensive WhatsApp automation solution that replaces Twilio with web-scraping and free AI bots for:

- **OTP Verification** - Send secure OTP codes via WhatsApp
- **Parcel Approval/Denial** - Interactive approval requests for deliveries
- **Smart Notifications** - AI-personalized messages for various events
- **Response Processing** - Automated handling of user responses

## 🛠️ Setup Instructions

### 1. Install Dependencies

The system uses Selenium for WhatsApp Web automation and AI services for intelligent messaging:

```bash
# Install Chrome WebDriver
pip install webdriver-manager selenium

# Install AI libraries
pip install openai google-generativeai

# Install other dependencies
pip install celery redis channels
```

### 2. Environment Variables

Add these to your `.env` file:

```bash
# WhatsApp Configuration
WHATSAPP_BUSINESS_NUMBER=+919876543210

# AI API Keys (Optional - system works without them)
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 3. Database Migration

```bash
python manage.py makemigrations notifications
python manage.py migrate
```

### 4. Set Up WhatsApp Session

```bash
# Interactive setup (will open browser for QR code scanning)
python manage.py setup_whatsapp --phone +919876543210

# With AI bot configuration
python manage.py setup_whatsapp --phone +919876543210 --setup-ai

# Headless mode (for production)
python manage.py setup_whatsapp --phone +919876543210 --headless
```

### 5. Start Celery Workers

```bash
# Start Celery worker for background tasks
celery -A smartlocker worker --loglevel=info

# Start Celery beat for scheduled tasks
celery -A smartlocker beat --loglevel=info
```

## 📱 Features

### WhatsApp Web Automation

- **Session Management**: Persistent WhatsApp Web sessions with QR code authentication
- **Message Sending**: Automated message delivery with retry mechanisms
- **Response Monitoring**: Real-time checking for user responses
- **Multi-format Support**: Text, OTP, and interactive approval messages

### AI-Powered Messaging

- **Smart OTP Generation**: AI-generated secure OTP codes
- **Message Personalization**: Context-aware message customization
- **Response Analysis**: Intelligent parsing of user responses
- **Multi-provider Support**: OpenAI GPT, Google Gemini, and fallback options

### Notification System

- **Template Management**: Flexible message templates for different scenarios
- **Multi-channel Support**: WhatsApp, SMS, Email, Push notifications
- **Priority Handling**: Urgent, high, medium, low priority levels
- **Retry Logic**: Automatic retry for failed deliveries

## 🔧 Usage Examples

### 1. Send Simple WhatsApp Message

```python
from notifications.utils import send_whatsapp_message

# Send a quick message
success = send_whatsapp_message("+919876543210", "Hello from Smart Locker! 🤖")
```

### 2. Send OTP via WhatsApp

```python
from notifications.utils import send_otp_to_user
from accounts.models import User

user = User.objects.get(username='john_doe')
otp_code = send_otp_to_user(user, "+919876543210", "login")
print(f"OTP sent: {otp_code}")
```

### 3. Send Parcel Approval Request

```python
from notifications.utils import WhatsAppMessenger

messenger = WhatsAppMessenger()
booking_details = {
    'recipient_name': 'John Doe',
    'sender_name': 'Amazon Delivery',
    'item_description': 'Electronics Package',
    'recipient_apartment': 'Apt 101, Building A'
}

success = messenger.send_parcel_approval_request("+919876543210", booking_details)
```

### 4. Send Personalized Notification

```python
from notifications.utils import SmartNotificationManager

manager = SmartNotificationManager()
context_data = {
    'booking_id': 'BK123456',
    'locker_number': 'L-A-001',
    'access_code': 'ABC123'
}

success = manager.send_personalized_notification(
    user=user,
    template_type='delivery_update',
    channel='whatsapp',
    context_data=context_data,
    priority='high'
)
```

### 5. Verify OTP

```python
from notifications.utils import verify_user_otp

is_valid = verify_user_otp(user, "123456", "login")
if is_valid:
    print("OTP verified successfully!")
```

## 🌐 API Endpoints

### WhatsApp Messaging

```bash
# Send WhatsApp message
POST /api/notifications/whatsapp/send-message/
{
    "phone_number": "+919876543210",
    "message": "Hello from Smart Locker!"
}

# Send approval request
POST /api/notifications/whatsapp/send-approval/
{
    "phone_number": "+919876543210",
    "booking_details": {
        "recipient_name": "John Doe",
        "sender_name": "Amazon",
        "item_description": "Package"
    }
}

# Check for responses
GET /api/notifications/whatsapp/check-responses/?phone_number=+919876543210
```

### OTP Management

```bash
# Send OTP
POST /api/notifications/otp/send/
{
    "phone_number": "+919876543210",
    "user_id": 1,
    "otp_type": "verification"
}

# Verify OTP
POST /api/notifications/otp/verify/
{
    "user_id": 1,
    "otp_code": "123456",
    "otp_type": "verification"
}
```

### System Status

```bash
# Get WhatsApp system status
GET /api/notifications/whatsapp/status/

Response:
{
    "active_sessions": 1,
    "recent_messages_24h": 25,
    "pending_approvals": 3,
    "active_ai_bots": 4,
    "system_status": "operational"
}
```

## 🤖 AI Bot Configuration

### Setting Up AI Bots

```python
from notifications.models import AIBotConfiguration

# OpenAI GPT for customer support
openai_bot = AIBotConfiguration.objects.create(
    name='Customer Support Bot',
    provider='openai',
    purpose='customer_support',
    model_name='gpt-3.5-turbo',
    api_key='your_openai_key',
    max_tokens=150,
    temperature=0.7,
    daily_limit=1000
)

# Google Gemini for message personalization
gemini_bot = AIBotConfiguration.objects.create(
    name='Message Personalizer',
    provider='google',
    purpose='message_personalization',
    model_name='gemini-pro',
    api_key='your_google_key',
    max_tokens=200,
    temperature=0.8,
    daily_limit=1500
)
```

### AI-Powered Features

1. **Smart OTP Generation**: Uses AI to generate more secure, random OTP codes
2. **Message Personalization**: Customizes messages based on user context and preferences
3. **Response Analysis**: Intelligently parses user responses to determine intent
4. **Language Support**: Can translate and localize messages for different users

## 📋 Management Commands

### Setup Commands

```bash
# Set up WhatsApp session
python manage.py setup_whatsapp --phone +919876543210 --setup-ai

# Test WhatsApp functionality
python manage.py test_whatsapp --phone +919876543210 --test-type all
```

### Testing Commands

```bash
# Test simple message
python manage.py test_whatsapp --phone +919876543210 --test-type message --message "Test message"

# Test OTP sending
python manage.py test_whatsapp --phone +919876543210 --test-type otp

# Test approval request
python manage.py test_whatsapp --phone +919876543210 --test-type approval
```

## 🔄 Background Tasks

The system uses Celery for asynchronous processing:

### Key Tasks

1. **send_notification_task**: Sends notifications asynchronously
2. **process_whatsapp_responses**: Checks for and processes user responses
3. **generate_ai_otp**: Generates OTP using AI services
4. **cleanup_expired_sessions**: Cleans up expired sessions and OTPs

### Scheduled Tasks

```python
# In celery.py, add periodic tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    'process-whatsapp-responses': {
        'task': 'notifications.tasks.process_whatsapp_responses',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'cleanup-expired-sessions': {
        'task': 'notifications.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}
```

## 🛡️ Security Features

### OTP Security

- **Time-based Expiration**: OTPs expire after 10 minutes
- **Attempt Limiting**: Maximum 3 verification attempts
- **AI Generation**: More secure random generation using AI
- **Phone Verification**: OTPs tied to specific phone numbers

### Session Security

- **Session Persistence**: WhatsApp sessions stored securely
- **Automatic Cleanup**: Expired sessions cleaned automatically
- **Error Handling**: Comprehensive error tracking and recovery

### Data Protection

- **Encrypted Storage**: Sensitive data encrypted in database
- **API Key Security**: API keys stored securely and not exposed
- **Audit Logging**: All messaging activities logged for audit

## 🚨 Troubleshooting

### Common Issues

1. **WhatsApp Session Expired**
   ```bash
   # Re-authenticate
   python manage.py setup_whatsapp --phone +919876543210
   ```

2. **Messages Not Sending**
   ```bash
   # Check session status
   python manage.py test_whatsapp --phone +919876543210 --test-type message
   ```

3. **AI Bot Not Working**
   ```bash
   # Verify API keys in environment
   echo $OPENAI_API_KEY
   echo $GOOGLE_API_KEY
   ```

4. **Celery Tasks Not Running**
   ```bash
   # Check Celery worker status
   celery -A smartlocker inspect active
   ```

### Monitoring

- **Admin Dashboard**: Monitor WhatsApp sessions and messages
- **API Status Endpoint**: Check system health via API
- **Celery Monitoring**: Use Flower for task monitoring
- **Log Analysis**: Check Django logs for detailed error information

## 📈 Performance Optimization

### Best Practices

1. **Session Reuse**: Keep WhatsApp sessions active to avoid re-authentication
2. **Batch Processing**: Process multiple messages in batches
3. **Caching**: Cache frequently used templates and configurations
4. **Rate Limiting**: Respect WhatsApp's rate limits to avoid blocks

### Scaling

- **Multiple Workers**: Run multiple Celery workers for high volume
- **Session Distribution**: Use multiple WhatsApp business accounts
- **Database Optimization**: Index frequently queried fields
- **Redis Caching**: Use Redis for session and temporary data storage

## 🔮 Future Enhancements

### Planned Features

1. **Multi-language Support**: Automatic language detection and translation
2. **Rich Media**: Support for images, documents, and voice messages
3. **Chatbot Integration**: Full conversational AI for customer support
4. **Analytics Dashboard**: Detailed messaging analytics and insights
5. **Webhook Integration**: Real-time webhook notifications for external systems

### Integration Possibilities

- **Voice Messages**: AI-generated voice OTPs
- **QR Code Generation**: Dynamic QR codes for locker access
- **Location Sharing**: Share locker locations via WhatsApp
- **Payment Links**: Send payment links for premium services

---

## 📞 Support

For technical support or questions about the WhatsApp automation system:

1. Check the Django admin panel for system status
2. Review the logs in `/var/log/smartlocker/`
3. Use the management commands for testing and diagnostics
4. Monitor Celery tasks for background processing issues

The system is designed to be robust and self-healing, with comprehensive error handling and automatic recovery mechanisms.