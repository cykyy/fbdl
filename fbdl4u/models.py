from django.db import models


# Create your models here.
from django.utils import timezone


class Job(models.Model):
    name = models.CharField(max_length=500)
    facebook = models.CharField(max_length=256)
    resolution = models.CharField(max_length=500, null=True)
    format = models.CharField(max_length=60, null=True)
    abs_path = models.CharField(max_length=500)
    user_agent = models.CharField(max_length=256, null=True)
    ip_addr = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # auto_now_add=True

    def __str__(self):
        return self.name[:50] + ' : ' + str(self.resolution)


class Contact(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    msg = models.CharField(max_length=256)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)  # auto_now_add=True
