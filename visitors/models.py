# visitors/models.py
from django.db import models
from core.models import TimeStampedModel

class Visitor(TimeStampedModel):
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)
    phone1 = models.CharField(max_length=30, blank=True)
    phone2 = models.CharField(max_length=30, blank=True)

    born_again = models.BooleanField(default=False)
    joining = models.BooleanField(default=False)
    need_visitation = models.BooleanField(default=False)

    prayer_request = models.TextField(blank=True)
    date = models.DateField(db_index=True)

    def __str__(self):
        return f"{self.full_name} ({self.date})"
    class Meta:
        ordering = ["-date"]    