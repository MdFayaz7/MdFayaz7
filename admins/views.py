from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from .models import Admin
from .forms import AdminLoginForm, UpdateFeeForm
from students.models import Student
from payments.models import Payment

def login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                admin = Admin.objects.get(username=username, is_active=True)
                if admin.check_password(password):
                    request.session['admin_id'] = str(admin.id)
                    request.session['admin_username'] = admin.username
                    messages.success(request, f'Welcome back, {admin.full_name}!')
                    return redirect('admins:dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except Admin.DoesNotExist:
                messages.error(request, 'Invalid username or account not found.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admins/login.html', {'form': form})

def dashboard(request):
    if 'admin_id' not in request.session:
        messages.error(request, 'Please login to access admin dashboard.')
        return redirect('admins:login')
    
    admin = get_object_or_404(Admin, id=request.session['admin_id'])
    
    # Dashboard statistics
    total_students = Student.objects.filter(is_active=True).count()
    total_payments = Payment.objects.filter(status='completed').count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    pending_payments = Payment.objects.filter(status='pending').count()
    
    # Recent payments
    recent_payments = Payment.objects.filter(status='completed').order_by('-created_at')[:10]
    
    # Fee type statistics
    fee_stats = Payment.objects.filter(status='completed').values('fee_type').annotate(
        count=Count('id'),
        total=Sum('amount')
    )
    
    context = {
        'admin': admin,
        'total_students': total_students,
        'total_payments': total_payments,
        'total_revenue': total_revenue,
        'pending_payments': pending_payments,
        'recent_payments': recent_payments,
        'fee_stats': fee_stats,
    }
    
    return render(request, 'admins/dashboard.html', context)

def students_list(request):
    if 'admin_id' not in request.session:
        messages.error(request, 'Please login to access admin dashboard.')
        return redirect('admins:login')
    
    search_query = request.GET.get('search', '')
    admission_type = request.GET.get('admission_type', '')
    
    students = Student.objects.filter(is_active=True)
    
    if search_query:
        students = students.filter(
            Q(college_id__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if admission_type:
        students = students.filter(admission_type=admission_type)
    
    students = students.order_by('college_id')
    
    # Pagination
    paginator = Paginator(students, 20)  # Show 20 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'admission_type': admission_type,
        'admission_choices': Student.ADMISSION_CHOICES,
    }
    
    return render(request, 'admins/students_list.html', context)

def update_student_fees(request, student_id):
    if 'admin_id' not in request.session:
        messages.error(request, 'Please login to access admin dashboard.')
        return redirect('admins:login')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = UpdateFeeForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Fee amounts updated successfully for {student.full_name}.')
            return redirect('admins:students_list')
    else:
        form = UpdateFeeForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
    }
    
    return render(request, 'admins/update_fees.html', context)

def student_payments(request, student_id):
    if 'admin_id' not in request.session:
        messages.error(request, 'Please login to access admin dashboard.')
        return redirect('admins:login')
    
    student = get_object_or_404(Student, id=student_id)
    payments = Payment.objects.filter(student=student).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(payments, 10)  # Show 10 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'student': student,
        'page_obj': page_obj,
    }
    
    return render(request, 'admins/student_payments.html', context)

def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admins:login')