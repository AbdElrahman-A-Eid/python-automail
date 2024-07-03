"""Main entry point of the application
"""
import os
from flask import Flask
from dotenv import load_dotenv
from auto_mail.email_sender import EmailSender
from auto_mail.web_app import WebApp

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The Flask application instance.
    """
    flask_app = Flask(__name__, static_folder='static')

    sender = os.environ.get('FROM_MAIL', '')
    sender_name = os.environ.get('FROM_NAME', '')
    password = os.environ.get('APP_PASS', '')
    email_sender = EmailSender(sender, sender_name, password)

    web_app = WebApp(flask_app, email_sender)
    web_app.setup_routes()

    return flask_app

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run(debug=True)
