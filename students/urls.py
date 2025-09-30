from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('logout/', views.logout, name='logout'),
    path('api/fee-amount/', views.get_fee_amount, name='get_fee_amount'),
]