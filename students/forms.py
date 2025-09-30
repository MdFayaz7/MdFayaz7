from django import forms
from django.core.exceptions import ValidationError
from .models import Student
import re

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = Student
        fields = ['college_id', 'email', 'full_name', 'phone_number', 'profile_picture', 'admission_type']
        widgets = {
            'college_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter College ID (e.g., CS2021001)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'admission_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_college_id(self):
        college_id = self.cleaned_data.get('college_id')
        if not re.match(r'^[A-Z0-9]+$', college_id):
            raise ValidationError('College ID must contain only uppercase letters and numbers')
        if Student.objects.filter(college_id=college_id).exists():
            raise ValidationError('This College ID is already registered')
        return college_id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered')
        return email
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError('Enter a valid phone number')
        return phone
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')
        return confirm_password
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Password must contain at least one letter')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number')
        return password

class StudentLoginForm(forms.Form):
    college_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter College ID'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )