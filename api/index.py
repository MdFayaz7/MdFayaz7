from http.server import BaseHTTPRequestHandler
import os
import sys

# Add the project directory to the sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_fee_system.settings')

try:
    # Import Django and set up the application
    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    
    # Get the WSGI application
    application = get_wsgi_application()
    
    # Import the necessary modules for handling requests
    from django.core.handlers.wsgi import WSGIRequest
    from io import BytesIO
    from urllib.parse import parse_qsl
    
    django_initialized = True
except Exception as e:
    django_initialized = False
    error_message = str(e)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not django_initialized:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Django initialization failed: {error_message}'.encode())
            return
            
        try:
            # Create a WSGIRequest
            environ = {
                'wsgi.input': BytesIO(),
                'wsgi.url_scheme': 'https',
                'wsgi.multiprocess': False,
                'wsgi.multithread': False,
                'wsgi.run_once': False,
                'REQUEST_METHOD': self.command,
                'PATH_INFO': self.path,
                'QUERY_STRING': '',
                'REMOTE_ADDR': self.client_address[0],
                'SERVER_NAME': self.server.server_name,
                'SERVER_PORT': str(self.server.server_port),
                'SERVER_PROTOCOL': self.request_version,
            }
            
            # Add headers to the environ
            for key, value in self.headers.items():
                environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
                
            # Create a Django request
            request = WSGIRequest(environ)
            
            # Process the request through Django
            response_status = '200 OK'
            response_headers = []
            
            def start_response(status, headers):
                nonlocal response_status, response_headers
                response_status = status
                response_headers = headers
            
            # Get the response from Django
            response_body = b''.join(application(environ, start_response))
            
            # Send the response
            status_code = int(response_status.split(' ')[0])
            self.send_response(status_code)
            
            for header, value in response_headers:
                self.send_header(header, value)
            
            self.end_headers()
            self.wfile.write(response_body)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error processing request: {str(e)}'.encode())
            
    def do_POST(self):
        self.do_GET()