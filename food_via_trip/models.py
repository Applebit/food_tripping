from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_id = models.IntegerField()
    entity_type = models.CharField(max_length=20)
    lat = models.FloatField()
    long = models.FloatField()
    address = models.CharField(max_length = 255, blank=True)

    def __str__(self):
        return self.address