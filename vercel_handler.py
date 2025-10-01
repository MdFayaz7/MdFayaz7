import os
from django.core.wsgi import get_wsgi_application

# Set up proper Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_fee_system.settings')

# Get the WSGI application
application = get_wsgi_application()

# Handler for Vercel serverless function
def handler(request, **kwargs):
    return application(request, **kwargs)