from django.shortcuts import render
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .models import Device, Capability, Command
from .serializers import (
    DeviceSerializer, CapabilitySerializer,
    CommandSerializer, ReadCommandSerializer, DeviceCommandSerializer
)

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all().order_by('name')
    serializer_class = DeviceSerializer

class CapabilityViewSet(viewsets.ModelViewSet):
    queryset = Capability.objects.all().order_by('name')
    serializer_class = CapabilitySerializer

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all().order_by('queued')
    serializer_class = CommandSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retreive']:
            return ReadCommandSerializer
        return super().get_serializer_class()


@api_view(['GET'])
def poll_device(request, device_id):
    queryset = Command.objects.filter(device_id=device_id, actioned=False).order_by('queued').first()

    serializer = DeviceCommandSerializer(queryset)

    queryset.actioned_time = datetime.datetime.now()
    queryset.actioned = True
    queryset.save()
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def poll(request):
    ''' Poll from device checking for any new commands '''
    print(request.data)
    
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def register(request):
    ''' Register new devices '''
    print(request.data)
    device_registration = request.data['registration']
    commands = request.data['capabilities']
    capabilities = []

    device, created = Device.objects.get_or_create(
        name = "",
        registration=device_registration,
        #capabilities=capabilities
    )
    device.save()

    for command in commands:
        capability, created = Capability.objects.get_or_create(name=command['command'], description=command['description'])
        device.capabilities.add(capability)

    device.save()

    return Response(data={'device_id': device.id}, status=status.HTTP_201_CREATED)
'''
    name = models.CharField(max_length=180)
    registration = models.UUIDField(unique=True)
    registered = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    capabilities = models.ManyToManyField(Capability)
'''


'''
class CommandViewSet(APIView):

    def get(self, request):


    def post(self, request):
        serializer = CommandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''


'''
# Create your views here.
class DeviceListApiView(APIView):

    def get(self, request, *args, **kwargs):
        if "device" in request.__dict__:
            devices = Device.objects.filter(id = request.device.id)
        else:
            devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name')
        }
        serializer = DeviceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''