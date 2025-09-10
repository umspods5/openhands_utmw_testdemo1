from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    
    # WhatsApp Session Management
    path('whatsapp/sessions/', views.WhatsAppSessionView.as_view(), name='whatsapp-sessions'),
    path('whatsapp/status/', views.whatsapp_status_api, name='whatsapp-status'),
    
    # WhatsApp Messaging
    path('whatsapp/send-message/', views.send_whatsapp_message_api, name='send-whatsapp-message'),
    path('whatsapp/send-approval/', views.send_approval_request_api, name='send-approval-request'),
    path('whatsapp/check-responses/', views.check_responses_api, name='check-responses'),
    path('whatsapp/process-responses/', views.process_responses_api, name='process-responses'),
    path('whatsapp/messages/', views.WhatsAppMessageView.as_view(), name='whatsapp-messages'),
    
    # OTP Management
    path('otp/send/', views.send_otp_api, name='send-otp'),
    path('otp/verify/', views.verify_otp_api, name='verify-otp'),
    path('otp/verifications/', views.OTPVerificationView.as_view(), name='otp-verifications'),
    
    # Personalized Notifications
    path('send-personalized/', views.send_personalized_notification_api, name='send-personalized-notification'),
]