from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class PersonalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_records")
    title = models.CharField(max_length=100)  # ex: "Deadlift"
    value = models.FloatField()  # ex: 120.5 (kg, chrono, etc.)
    unit = models.CharField(max_length=10, default="kg")  # ou "sec", "m", etc.
    date = models.DateField(default=date.today)
    weight = models.FloatField()
    description = models.TextField(blank=True, null=True)  # Optional description of the record

    @property
    def bodyweight(self):
        if self.unit == "kg" and self.weight:
            try:
                return (self.value + self.weight) / self.weight * 100
            except ZeroDivisionError:
                return None
        return None
    
    def __str__(self):
        return f"{self.title} - {self.value} {self.unit}"