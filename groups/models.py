from django.db import models
from core.models import TimeStampedModel
from members.models import Member


class GroupType(models.TextChoices):
    MINISTRY = "MINISTRY", "Ministry Group"
    SERVICE = "SERVICE", "Service Group"


class Group(TimeStampedModel):
    group_type = models.CharField(max_length=10, choices=GroupType.choices)
    name = models.CharField(max_length=150, unique=True)

    leader = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="leading_groups",
        help_text="Optional: group leader"
    )

    members = models.ManyToManyField(Member, blank=True, related_name="church_groups")

    class Meta:
        ordering = ["group_type", "name"]

    def __str__(self):
        return f"{self.get_group_type_display()}: {self.name}"

    @property
    def members_count(self):
        return self.members.count()

