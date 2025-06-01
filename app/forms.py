from django import forms
from .models import PersonalRecord

EXERCISE_CHOICES = [
    ("Weighted Pull-up 1rpm", "Weighted Pull-up 1rpm"),
    ("Weighted Pull-up 2rpm", "Weighted Pull-up 2rpm"),
    ("Finger Strength 20mm half crimp 7sm", "Finger Strength 20mm half crimp 7sm"),
    ("Power endurance 20mm half crimp 60%m", "Power endurance 20mm half crimp 60%m"),
]

class PersonalRecordForm(forms.ModelForm):
    title = forms.ChoiceField(choices=EXERCISE_CHOICES, label="Exercice")

    class Meta:
        model = PersonalRecord
        fields = ["title", "value", "unit", "date", "weight"]
