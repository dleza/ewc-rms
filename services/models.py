# services/models.py
from django.db import models
from core.models import TimeStampedModel


class ActivityType(models.TextChoices):
    SUNDAY_SERVICE = "SUNDAY_SERVICE", "Sunday Service"
    MIDWEEK = "MIDWEEK", "Midweek Service"
    PRAYER = "PRAYER", "Prayer Meeting"
    YOUTH = "YOUTH", "Youth Meeting"
    OTHER = "OTHER", "Other"


class AttendanceRecord(TimeStampedModel):
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    group = models.ForeignKey("groups.Group", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(db_index=True)

    adult_female = models.PositiveIntegerField(default=0)
    adult_male = models.PositiveIntegerField(default=0)
    teen_female = models.PositiveIntegerField(default=0)
    teen_male = models.PositiveIntegerField(default=0)
    children_female = models.PositiveIntegerField(default=0)
    children_male = models.PositiveIntegerField(default=0)

    preacher = models.CharField(max_length=200, blank=True)
    title_of_msg = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [models.Index(fields=["date", "activity_type"])]

    @property
    def total_attendance(self):
        return (
            self.adult_female + self.adult_male +
            self.teen_female + self.teen_male +
            self.children_female + self.children_male
        )

    def __str__(self):
        return f"{self.date} - {self.activity_type} - {self.total_attendance}"


