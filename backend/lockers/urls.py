from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'banks', views.LockerBankViewSet)
router.register(r'lockers', views.LockerViewSet)
router.register(r'access', views.LockerAccessViewSet)
router.register(r'maintenance', views.LockerMaintenanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('available/', views.AvailableLockerListView.as_view(), name='available-lockers'),
    path('<int:locker_id>/status/', views.LockerStatusView.as_view(), name='locker-status'),
    path('<int:locker_id>/control/', views.LockerControlView.as_view(), name='locker-control'),
]