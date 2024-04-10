from django import forms
from .models import Workout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from datetime import date
import datetime

class CustomUserCreationForm(UserCreationForm):
    # Assuming SEX_CHOICES and WEIGHT_UNIT_CHOICES are defined in UserProfile
    sex = forms.ChoiceField(choices=UserProfile.SEX_CHOICES)
    body_weight = forms.DecimalField(max_digits=5, decimal_places=2)
    weight_unit = forms.ChoiceField(choices=UserProfile.WEIGHT_UNIT_CHOICES)
    
    # Separate fields for the birth date components
    birth_year = forms.ChoiceField(label='Year', choices=[(y, y) for y in range(1900, date.today().year+1)])
    birth_month = forms.ChoiceField(label='Month', choices=[(m, m) for m in range(1, 13)])
    birth_day = forms.ChoiceField(label='Day', choices=[(d, d) for d in range(1, 32)])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'sex', 'body_weight', 'weight_unit', 'birth_year', 'birth_month', 'birth_day']

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Process the birth date fields
        birth_year = int(self.cleaned_data['birth_year'])
        birth_month = int(self.cleaned_data['birth_month'])
        birth_day = int(self.cleaned_data['birth_day'])
        birth_date = date(birth_year, birth_month, birth_day)
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                sex=self.cleaned_data['sex'],
                body_weight=self.cleaned_data['body_weight'],
                weight_unit=self.cleaned_data['weight_unit'],
                birth_date=birth_date,  # Use the combined birth date
            )
        return user

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
        self.fields['date'].required = False
        self.fields['time'].widget = forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}, format='%H:%M')
        self.fields['time'].required = False
        self.fields['location'].required = False

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        # Attempt to create a date object only for validation purposes here
        if day and month and year:
            try:
                day = int(day)
                month = int(month)
                year = int(year)
                cleaned_data['date'] = datetime.date(year, month, day)  # Store the valid date object in cleaned_data
            except ValueError as e:
                raise forms.ValidationError(f'Invalid date: {e}')

        return cleaned_data

