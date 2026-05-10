from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Request, Reservation
from clubhouse.models import Club, Location


class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ['club', 'type', 'notes', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']
        if profile is not None:
            self.fields['club'].queryset = (
                profile.club_officer.filter(approved=True) |
                profile.faculty_advisor.filter(approved=True)
            ).distinct()
        else:
            self.fields['club'].queryset = Club.objects.none()

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now() + timedelta(weeks=1):
            raise forms.ValidationError(
                'Requests must be submitted at least one week in advance. '
                'For urgent requests, please contact Student Engagement directly.'
            )
        return due_date


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['location', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['location'].queryset = Location.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data


class StandaloneReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['club', 'location', 'start_time', 'end_time', 'purpose']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'purpose': forms.TextInput(attrs={'placeholder': 'e.g. Weekly officer meeting'}),
        }

    def __init__(self, *args, profile=None, initial_club=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['location'].queryset = Location.objects.all()
        self.fields['purpose'].required = False

        if profile is not None:
            clubs = (
                profile.club_officer.filter(approved=True, denied=False) |
                profile.faculty_advisor.filter(approved=True, denied=False)
            ).distinct()
            if profile.role == profile.Role.ADMIN:
                clubs = Club.objects.filter(approved=True, denied=False)
            self.fields['club'].queryset = clubs
        else:
            self.fields['club'].queryset = Club.objects.none()

        if initial_club is not None:
            self.fields['club'].initial = initial_club

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data
