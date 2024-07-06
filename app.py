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

    sender = os.environ.get('PYAUTO_FROM_MAIL', '')
    sender_name = os.environ.get('PYAUTO_FROM_NAME', '')
    password = os.environ.get('PYAUTO_APP_PASS', '')
    num_processes = int(os.environ.get('PYAUTO_NUM_PROCESSES', 1))
    email_sender = EmailSender(sender, sender_name, password, num_processes)

    web_app = WebApp(flask_app, email_sender)
    web_app.setup_routes()

    return flask_app

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run(debug=True)
