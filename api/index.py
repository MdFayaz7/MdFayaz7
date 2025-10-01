import os
import sys

# Add the project directory to the sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_fee_system.settings')

# Import Django and set up the application
from django.core.wsgi import get_wsgi_application
from django.conf import settings

# Get the WSGI application
application = get_wsgi_application()

# Handler for Vercel
def handler(request, **kwargs):
    return application(request, **kwargs)