from django import forms
from .models import FoodLog, WorkoutSet

class FoodLogForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        # List fields you want in the form. Exclude 'user' as we'll set it automatically.
        fields = ['date', 'day_of_week', 'time', 'calories', 'proteins', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'day_of_week': forms.TextInput(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'proteins': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required if they aren't by default based on the model
        for field_name in self.fields:
             self.fields[field_name].required = True


class WorkoutSetForm(forms.ModelForm):
    class Meta:
        model = WorkoutSet
        fields = ['exercise_name', 'weight', 'reps', 'sets', 'notes']
        widgets = {
            'exercise_name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }