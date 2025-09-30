from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid

class Admin(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'admins'
    
    def __str__(self):
        return f"{self.username} - {self.full_name}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)