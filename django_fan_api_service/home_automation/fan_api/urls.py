from django.urls import path, include
from .views import DeviceViewSet, CapabilityViewSet, CommandViewSet, poll, poll_device, register
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'capabilities', CapabilityViewSet)
router.register(r'commands', CommandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('commands/', CommandViewSet.as_view()),
    path('register/', register),
    path('poll/', poll),
    path('poll/<int:device_id>', poll_device)
]