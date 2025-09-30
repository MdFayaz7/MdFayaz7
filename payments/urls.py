from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay-fee/', views.pay_fee, name='pay_fee'),
    path('create-order/', views.create_order, name='create_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('download-receipt/<str:payment_id>/', views.download_receipt, name='download_receipt'),
    path('payment-success/<str:payment_id>/', views.payment_success, name='payment_success'),
]