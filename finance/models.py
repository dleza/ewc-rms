# finance/models.py
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from core.models import TimeStampedModel


class BudgetCategory(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BudgetPeriodType(models.TextChoices):
    WEEKLY = "WEEKLY", "Weekly"
    MONTHLY = "MONTHLY", "Monthly"
    ANNUAL = "ANNUAL", "Annual"


class BudgetPlan(TimeStampedModel):
    period_type = models.CharField(max_length=10, choices=BudgetPeriodType.choices)
    name = models.CharField(max_length=150)  # e.g. "2026 Annual Budget"
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    approved_by = models.CharField(max_length=200, blank=True)
    approved_on = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("period_type", "start_date", "end_date")
        ordering = ["-start_date"]

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date must be on/after start date.")

    @property
    def total_allocated(self):
        return self.lines.aggregate(total=models.Sum("amount_allocated"))["total"] or Decimal("0.00")

    def __str__(self):
        return self.name


class BudgetLine(TimeStampedModel):
    plan = models.ForeignKey(BudgetPlan, on_delete=models.CASCADE, related_name="lines")
    category = models.ForeignKey(BudgetCategory, on_delete=models.PROTECT)
    amount_allocated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        unique_together = ("plan", "category")
        ordering = ["category__name"]

    def __str__(self):
        return f"{self.plan} - {self.category}"


class Expense(TimeStampedModel):
    date = models.DateField(db_index=True)
    category = models.ForeignKey(BudgetCategory, on_delete=models.PROTECT)

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    paid_to = models.CharField(max_length=200, blank=True)
    reference_no = models.CharField(max_length=80, blank=True)  # receipt/invoice
    recorded_by = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.date} - {self.category} - {self.amount}"

class CollectionCategory(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    # optional flags (useful for reporting)
    is_tithe = models.BooleanField(default=False)
    is_offering = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MeetingCollection(TimeStampedModel):
    date = models.DateField(db_index=True)
    name_of_counter = models.CharField(max_length=150)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Collections {self.date}"

    @property
    def total(self):
        return self.entries.aggregate(total=models.Sum("amount"))["total"] or Decimal("0.00")


class CollectionEntry(TimeStampedModel):
    collection = models.ForeignKey(
        MeetingCollection,
        on_delete=models.CASCADE,
        related_name="entries"
    )
    category = models.ForeignKey(
        CollectionCategory,
        on_delete=models.PROTECT,
        related_name="entries"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ("collection", "category")
        ordering = ["category__name"]

    def __str__(self):
        return f"{self.collection.date} - {self.category.name}: {self.amount}"

class CollectionDetail(TimeStampedModel):
    collection = models.ForeignKey(MeetingCollection, on_delete=models.CASCADE, related_name="details")
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.collection.date} - {self.description} - {self.amount}"