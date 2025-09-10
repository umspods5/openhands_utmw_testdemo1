from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)
router.register(r'routes', views.DeliveryRouteViewSet)
router.register(r'photos', views.BookingPhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateBookingView.as_view(), name='create-booking'),
    path('<uuid:booking_id>/status/', views.BookingStatusView.as_view(), name='booking-status'),
    path('<uuid:booking_id>/track/', views.TrackBookingView.as_view(), name='track-booking'),
    path('<uuid:booking_id>/approve/', views.ApproveBookingView.as_view(), name='approve-booking'),
    path('<uuid:booking_id>/cancel/', views.CancelBookingView.as_view(), name='cancel-booking'),
    path('agent/available/', views.AvailableBookingsView.as_view(), name='available-bookings'),
    path('agent/assign/', views.AssignBookingView.as_view(), name='assign-booking'),
]