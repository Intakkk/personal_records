from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PersonalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_records")
    title = models.CharField(max_length=100)  # ex: "Deadlift"
    value = models.FloatField()  # ex: 120.5 (kg, chrono, etc.)
    unit = models.CharField(max_length=10, default="kg")  # ou "sec", "m", etc.
    date = models.DateField(auto_now_add=True)  # Date of the record
    description = models.TextField(blank=True, null=True)  # Optional description of the record
    
    def __str__(self):
        return f"{self.title} - {self.value} {self.unit}"