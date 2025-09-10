# Smart Locker System

A comprehensive smart locker solution for apartment buildings, supporting parcel delivery, document exchange, laundry services, and food delivery with temperature control.

## 🏗️ Architecture Overview

```
Smart Locker System
├── Backend (Django + PostgreSQL)
├── Web Dashboards (React.js)
│   ├── Admin/Support Dashboard
│   ├── Delivery Agent Dashboard
│   └── Client User Dashboard
├── Mobile App (React Native)
├── Kiosk Interface (Kivy)
├── Hardware Integration (Arduino + STM32)
└── Cloud Infrastructure (AWS)
```

## 🚀 Features

### Core Functionality
- **Multi-purpose Lockers**: Parcels, documents, laundry, hot/cold food
- **Temperature Control**: Separate zones for different item types
- **User Management**: Residents, delivery agents, support staff
- **Real-time Tracking**: Live status updates and notifications
- **Secure Access**: QR codes, OTP verification, biometric options

### Payment & Messaging
- **Payment Gateway**: Razorpay integration
- **Notifications**: WhatsApp messaging + web scraping + AI Bot + Free API 
- **Multi-language Support**: Localized interfaces

### Analytics & Monitoring
- **Usage Analytics**: Locker utilization, peak hours, revenue
- **Maintenance Alerts**: Hardware status monitoring
- **Delivery Insights**: Agent performance, delivery times

## 📱 User Interfaces

### 1. Admin/Support Dashboard
- Locker management and configuration
- User account management
- System monitoring and analytics
- Maintenance scheduling
- Revenue tracking

### 2. Delivery Agent Dashboard
- Active delivery assignments
- Locker availability and booking
- Route optimization
- Performance metrics
- Earnings tracking

### 3. Client User Dashboard
- Locker booking and management
- Delivery tracking
- Payment history
- Notification preferences
- Support tickets

### 4. Mobile App (iOS & Android)
- QR code scanning for locker access
- Push notifications
- Real-time delivery tracking
- In-app payments
- Emergency support

### 5. Kiosk Interface
- Touch-screen locker operations
- User authentication
- Payment processing
- Multi-language support
- Accessibility features

## 🛠️ Technology Stack

- **Backend**: Django (Python) + PostgreSQL
- **Web Frontend**: React.js + Material-UI
- **Mobile**: React Native
- **Kiosk**: Kivy (Python)
- **Hardware**: Arduino + STM32 (C)
- **Cloud**: AWS (EC2, S3, RDS)
- **Payments**: Razorpay
- **Messaging**: Twilio + WhatsApp Business API
- **Real-time**: WebSockets + Redis

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+
- Redis
- Arduino IDE

### Installation

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. **Web Dashboards**
```bash
cd web-dashboards/admin
npm install
npm start
```

3. **Mobile App**
```bash
cd mobile-app
npm install
npx react-native run-android  # or run-ios
```

4. **Kiosk Interface**
```bash
cd kiosk
pip install -r requirements.txt
python main.py
```

## 📊 API Documentation

The backend provides RESTful APIs for all operations:
- Authentication & User Management
- Locker Operations
- Booking & Delivery Management
- Payment Processing
- Notifications & Messaging
- Analytics & Reporting

API documentation is available at `/api/docs/` when running the backend.

## 🔧 Hardware Integration

The system communicates with Arduino/STM32 controllers for:
- Locker door control (servo motors)
- Temperature monitoring (sensors)
- Occupancy detection (weight/proximity sensors)
- Status LED indicators
- Emergency unlock mechanisms

## 🚀 Deployment

### AWS Infrastructure
- **EC2**: Application servers
- **RDS**: PostgreSQL database
- **S3**: File storage and backups
- **CloudFront**: CDN for web assets
- **ElastiCache**: Redis for caching
- **SES**: Email notifications

### Docker Support
All components include Dockerfiles for containerized deployment.

## 📈 Monitoring & Analytics

- **System Health**: Uptime, performance metrics
- **Business Metrics**: Revenue, usage patterns
- **User Analytics**: Engagement, satisfaction
- **Hardware Status**: Locker health, maintenance needs

## 🔒 Security

- **Data Encryption**: End-to-end encryption for sensitive data
- **Access Control**: Role-based permissions
- **Audit Logging**: Complete activity tracking
- **Secure Communications**: HTTPS/WSS for all connections
- **Hardware Security**: Tamper detection and alerts

## 📞 Support

For technical support or business inquiries, contact the development team.

## 📄 License

Proprietary software - All rights reserved.