
""" class MeetingCollection(TimeStampedModel):
    date = models.DateField(db_index=True)

    total_offering = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_tithe = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_first_fruits = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_seed_offering = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    name_of_counter = models.CharField(max_length=200)

    class Meta:
        ordering = ["-date", "-id"]

    @property
    def total(self):
        return self.total_offering + self.total_tithe + self.total_first_fruits + self.total_seed_offering

    def __str__(self):
        return f"{self.date} - {self.total}" """