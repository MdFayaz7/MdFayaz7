from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from students.models import Student
from .models import Payment
from .utils import generate_receipt_pdf
import razorpay
import json
import hmac
import hashlib
import requests
import time

# Initialize Razorpay client with timeout settings
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# Configure the underlying requests session with timeouts
razorpay_client.session.request = lambda *args, **kwargs: requests.Session().request(
    *args, **{**kwargs, 'timeout': 10}  # 10 seconds timeout
)

def pay_fee(request):
    if 'student_id' not in request.session:
        messages.error(request, 'Please login to make payments.')
        return redirect('students:login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    
    context = {
        'student': student,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'fee_amounts': {
            'college_fee': float(student.college_fee),
            'exam_fee': float(student.exam_fee),
            'bus_fee': float(student.bus_fee),
        }
    }
    return render(request, 'payments/pay_fee.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        data = json.loads(request.body)
        fee_type = data.get('fee_type')
        
        student = get_object_or_404(Student, id=request.session['student_id'])
        
        # Get fee amount based on type
        fee_amounts = {
            'college_fee': student.college_fee,
            'exam_fee': student.exam_fee,
            'bus_fee': student.bus_fee,
        }
        
        if fee_type not in fee_amounts:
            return JsonResponse({'error': 'Invalid fee type'}, status=400)
        
        amount = fee_amounts[fee_type]
        amount_in_paise = int(float(amount) * 100)  # Convert to paise
        
        # For testing purposes, generate a mock order ID
        import uuid
        mock_order_id = f"order_{uuid.uuid4().hex[:16]}"
        
        # Create payment record with mock order ID
        payment = Payment.objects.create(
            student=student,
            fee_type=fee_type,
            amount=amount,
            razorpay_order_id=mock_order_id,
            status='pending'
        )
        
        # Return mock order data for testing
        return JsonResponse({
            'order_id': mock_order_id,
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_id': str(payment.id)
        })
                
    except Exception as e:
        return JsonResponse({'error': f'Request processing error: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def verify_payment(request):
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id', 'mock_payment_id')
        razorpay_signature = data.get('razorpay_signature', 'mock_signature')
        
        # For mock payment system, we'll automatically approve all payments
        # Find the payment by order ID
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            
            # Update payment record
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'completed'
            payment.save()
            
            # Generate receipt number
            receipt_number = payment.generate_receipt_number()
            
            return JsonResponse({
                'success': True,
                'payment_id': str(payment.id),
                'receipt_number': receipt_number
            })
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment record not found'}, status=404)
            
    except Exception as e:
        return JsonResponse({'error': f'Payment verification error: {str(e)}'}, status=500)

def download_receipt(request, payment_id):
    if 'student_id' not in request.session:
        messages.error(request, 'Please login to download receipts.')
        return redirect('students:login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    payment = get_object_or_404(Payment, id=payment_id, student=student, status='completed')
    
    # Generate PDF receipt
    pdf_buffer = generate_receipt_pdf(payment)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.receipt_number}.pdf"'
    
    # Mark receipt as generated
    payment.receipt_generated = True
    payment.save()
    
    return response

def payment_success(request, payment_id):
    if 'student_id' not in request.session:
        messages.error(request, 'Please login to view payment details.')
        return redirect('students:login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    payment = get_object_or_404(Payment, id=payment_id, student=student)
    
    return render(request, 'payments/payment_success.html', {
        'payment': payment,
        'student': student
    })