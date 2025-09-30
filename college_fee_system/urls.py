from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('students:login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('students/', include('students.urls')),
    path('payments/', include('payments.urls')),
    path('admins/', include('admins.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)