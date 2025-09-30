from django import forms
from django.core.exceptions import ValidationError
from .models import Admin
from students.models import Student

class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

class UpdateFeeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['college_fee', 'exam_fee', 'bus_fee']
        widgets = {
            'college_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'exam_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'bus_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
    
    def clean_college_fee(self):
        fee = self.cleaned_data.get('college_fee')
        if fee < 0:
            raise ValidationError('Fee amount cannot be negative')
        return fee
    
    def clean_exam_fee(self):
        fee = self.cleaned_data.get('exam_fee')
        if fee < 0:
            raise ValidationError('Fee amount cannot be negative')
        return fee
    
    def clean_bus_fee(self):
        fee = self.cleaned_data.get('bus_fee')
        if fee < 0:
            raise ValidationError('Fee amount cannot be negative')
        return fee