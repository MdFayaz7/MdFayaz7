from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator
import uuid

class Student(models.Model):
    ADMISSION_CHOICES = [
        ('counseling', 'Counseling'),
        ('management', 'Management'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    college_id = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(regex=r'^[A-Z0-9]+$', message='College ID must contain only uppercase letters and numbers')
    ])
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be valid')
    ])
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    password = models.CharField(max_length=128)
    admission_type = models.CharField(max_length=20, choices=ADMISSION_CHOICES, default='counseling')
    
    # Fee amounts (can be updated by admin)
    college_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    bus_fee = models.DecimalField(max_digits=10, decimal_places=2, default=15000.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'students'
        
    def __str__(self):
        return f"{self.college_id} - {self.full_name}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def get_total_fees(self):
        return self.college_fee + self.exam_fee + self.bus_fee