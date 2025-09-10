from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'methods', views.PaymentMethodViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'plans', views.PaymentPlanViewSet)
router.register(r'subscriptions', views.UserSubscriptionViewSet)
router.register(r'invoices', views.InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-order/', views.CreatePaymentOrderView.as_view(), name='create-payment-order'),
    path('verify-payment/', views.VerifyPaymentView.as_view(), name='verify-payment'),
    path('webhook/razorpay/', views.RazorpayWebhookView.as_view(), name='razorpay-webhook'),
    path('refund/', views.RefundPaymentView.as_view(), name='refund-payment'),
]