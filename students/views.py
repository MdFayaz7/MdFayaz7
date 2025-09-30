from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
from .forms import StudentRegistrationForm, StudentLoginForm
from payments.models import Payment
import json

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])
            student.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('students:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'students/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            college_id = form.cleaned_data['college_id']
            password = form.cleaned_data['password']
            
            try:
                student = Student.objects.get(college_id=college_id, is_active=True)
                if student.check_password(password):
                    request.session['student_id'] = str(student.id)
                    request.session['college_id'] = student.college_id
                    messages.success(request, f'Welcome back, {student.full_name}!')
                    return redirect('students:dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid College ID or account not found.')
    else:
        form = StudentLoginForm()
    
    return render(request, 'students/login.html', {'form': form})

def dashboard(request):
    if 'student_id' not in request.session:
        messages.error(request, 'Please login to access dashboard.')
        return redirect('students:login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    recent_payments = Payment.objects.filter(student=student).order_by('-created_at')[:5]
    
    context = {
        'student': student,
        'recent_payments': recent_payments,
    }
    return render(request, 'students/dashboard.html', context)

def profile(request):
    if 'student_id' not in request.session:
        messages.error(request, 'Please login to access profile.')
        return redirect('students:login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    return render(request, 'students/profile.html', {'student': student})

def payment_history(request):
    if 'student_id' not in request.session:
        messages.error(request, 'Please login to access payment history.')
        return redirect('students:login')
    
    student = get_object_or_404(Student, id=request.session['student_id'])
    payments = Payment.objects.filter(student=student).order_by('-created_at')
    
    return render(request, 'students/payment_history.html', {
        'student': student,
        'payments': payments
    })

def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('students:login')

@csrf_exempt
@require_http_methods(["GET"])
def get_fee_amount(request):
    if 'student_id' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    fee_type = request.GET.get('fee_type')
    student = get_object_or_404(Student, id=request.session['student_id'])
    
    fee_amounts = {
        'college_fee': float(student.college_fee),
        'exam_fee': float(student.exam_fee),
        'bus_fee': float(student.bus_fee),
    }
    
    if fee_type in fee_amounts:
        return JsonResponse({'amount': fee_amounts[fee_type]})
    else:
        return JsonResponse({'error': 'Invalid fee type'}, status=400)