from rest_framework import serializers
from .models import Device, Capability, Command

class CapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Capability
        fields = ["id", "name"]

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "registered", "last_update", "capabilities"]

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ["id", "device", "capability"]

class ReadCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ["id", "device", "capability", "actioned", "queued", "actioned_time"]

class DeviceCommandSerializer(serializers.ModelSerializer):
    capability_name = serializers.CharField(source='capability.name')

    class Meta:
        model = Command
        fields = ["capability_name"]