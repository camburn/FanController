from django.db import models


class Capability(models.Model):
    name = models.CharField(max_length=180, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.__class__.__name__}: {self.id} - {self.name}'

class Device(models.Model):
    name = models.CharField(max_length=180)
    registration = models.UUIDField(unique=True)
    registered = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    capabilities = models.ManyToManyField(Capability)

class Command(models.Model):
    device = models.ForeignKey("Device", on_delete=models.CASCADE)
    capability = models.ForeignKey("Capability", on_delete=models.CASCADE)
    actioned = models.BooleanField(default=False)
    queued = models.DateTimeField(auto_now_add=True)
    actioned_time = models.DateTimeField(blank=True, null=True)
