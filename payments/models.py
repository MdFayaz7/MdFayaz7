from django.db import models
from students.models import Student
import uuid

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    FEE_TYPE_CHOICES = [
        ('college_fee', 'College Fee'),
        ('exam_fee', 'Exam Fee'),
        ('bus_fee', 'Bus Fee'),
    ]
    
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Receipt details
    receipt_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    receipt_generated = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.college_id} - {self.get_fee_type_display()} - ₹{self.amount}"
    
    def generate_receipt_number(self):
        if not self.receipt_number:
            import datetime
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            self.receipt_number = f"RCP{date_str}{str(self.id)[:8].upper()}"
            self.save()
        return self.receipt_number