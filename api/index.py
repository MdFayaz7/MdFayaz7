from http.server import BaseHTTPRequestHandler

def handler(request, context):
    """
    Simple serverless function handler for Vercel
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>College Fee System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 {
                    color: #2c3e50;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .message {
                    background-color: #f8f9fa;
                    border-left: 4px solid #4CAF50;
                    padding: 15px;
                    margin-bottom: 20px;
                }
                .error {
                    background-color: #fff8f8;
                    border-left: 4px solid #FF5252;
                    padding: 15px;
                    margin-bottom: 20px;
                }
                .info {
                    margin-top: 30px;
                    font-size: 0.9em;
                }
                code {
                    background-color: #f5f5f5;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                }
            </style>
        </head>
        <body>
            <h1>College Fee System</h1>
            <div class="message">
                <p>The application is currently being deployed to Vercel.</p>
                <p>We're working on resolving deployment issues. Please check back soon.</p>
            </div>
            <div class="info">
                <p>This is a temporary landing page while we fix the deployment issues.</p>
                <p>If you're the administrator, please check the Vercel logs for more details.</p>
            </div>
        </body>
        </html>
        """
    }