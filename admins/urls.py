from django.urls import path
from . import views

app_name = 'admins'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students_list, name='students_list'),
    path('students/<str:student_id>/fees/', views.update_student_fees, name='update_student_fees'),
    path('students/<str:student_id>/payments/', views.student_payments, name='student_payments'),
    path('logout/', views.logout, name='logout'),
]