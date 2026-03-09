GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"

NO_SUBJECT_LINE = "No subject line available"
NO_EMAIL_BODY = "No email body available"
ERROR_MESSAGE = "An Error Occurred"

MAILGUN_BASE_URL = "https://api.mailgun.net"

DEFAULT_HTML_PREVIEW = """
<html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                max-height: 300px;
                margin: auto;
            }
            h1 {
                color: #333;
            }
            p {
                color: #555;
                line-height: 1.6;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Your Email Preview will appear here</h1>
            <p>Nothing to preview yet Click on "Looks Good! Preview Email" to generate an HTML preview of your generated email.</p>
        </div>
    </body>
</html>"""