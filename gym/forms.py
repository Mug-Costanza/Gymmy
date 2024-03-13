from django import forms
from .models import Workout
from datetime import date
import datetime

class WorkoutForm(forms.ModelForm):
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    # Correct the days choices to be in the (value, display) format
    days = [(day, str(day)) for day in range(1, 32)]
    years = [(year, str(year)) for year in range(2024, 1900, -1)]  # Adjust the range as needed

    month = forms.ChoiceField(choices=months, label='Month', widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_month'}))
    day = forms.ChoiceField(choices=days, label='Day', widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_day'}))
    year = forms.ChoiceField(choices=years, label='Year', widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_year'}))

    class Meta:
        model = Workout
        fields = ['type', 'duration', 'date', 'time', 'location']
        labels = {
            'type': 'Type',
            'duration': 'Duration (minutes)',
            'date': 'Date',
            'time': 'Time (Optional)',
            'location': 'Location (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        today = date.today()
        
        self.fields['month'].initial = today.month
        self.fields['day'].initial = today.day
        self.fields['year'].initial = today.year

        self.fields['type'].required = True
        self.fields['duration'].required = True
        self.fields['date'].required = True
        self.fields['time'].widget = forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M')
        self.fields['time'].required = False
        self.fields['location'].required = False
    
    def clean_date(self):
        day = self.cleaned_data.get('day')
        month = self.cleaned_data.get('month')
        year = self.cleaned_data.get('year')
        if day and month and year:
            try:
                # Convert day, month, and year to integers
                day = int(day)
                month = int(month)
                year = int(year)
                return datetime.date(year, month, day)
            except ValueError:
                raise forms.ValidationError('Invalid date.')
        return None
    
    def clean(self):
        cleaned_data = super().clean()
        date = self.clean_date()  # Call clean_date method
        if date:
            cleaned_data['date'] = date
        return cleaned_data


