from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/(?P<user_id>\w+)/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/locker-status/(?P<locker_id>\w+)/$', consumers.LockerStatusConsumer.as_asgi()),
    re_path(r'ws/delivery-tracking/(?P<booking_id>\w+)/$', consumers.DeliveryTrackingConsumer.as_asgi()),
]