from django.db import models
from core.models import TimeStampedModel

class Gender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"

class AgeCategory(models.TextChoices):
    CHILD = "CHILD", "Child"
    TEEN = "TEEN", "Teen"
    ADULT = "ADULT", "Adult"

class MaritalStatus(models.TextChoices):
    SINGLE = "SINGLE", "Single"
    MARRIED = "MARRIED", "Married"
    DIVORCED = "DIVORCED", "Divorced"
    WIDOWED = "WIDOWED", "Widowed"

class Member(TimeStampedModel):
    member_no = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    age_category = models.CharField(max_length=10, choices=AgeCategory.choices)
    date_of_join = models.DateField()
    date_of_renewal = models.DateField(null=True, blank=True)

    address = models.CharField(max_length=255)
    area = models.CharField(max_length=120, blank=True)
    house_no = models.CharField(max_length=50, blank=True)

    email = models.EmailField(blank=True)
    phone1 = models.CharField(max_length=30)
    phone2 = models.CharField(max_length=30, blank=True)

    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices, blank=True)

    def __str__(self):
        return f"{self.member_no} - {self.full_name}"
