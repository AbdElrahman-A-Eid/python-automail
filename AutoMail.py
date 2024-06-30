# Load your env variables
from dotenv import load_dotenv
load_dotenv()

import re
import os
import csv
import smtplib
from glob import glob
from pathlib import Path
from jinja2 import Template
from datetime import datetime
from traceback import format_exc
from flask_session import Session
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import Flask, render_template, request, flash, redirect, url_for, session

class EmailSender:
    def __init__(self, sender, sender_name, password):
        self.sender = sender
        self.sender_name = sender_name
        self.password = password

    def send_email(self, subject, body, parts, recipient, recipient_name):
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f'{self.sender_name} <{self.sender}>'
        message['To'] = f'{recipient_name} <{recipient}>'
        text_part = MIMEText(body, 'html')
        message.attach(text_part)

        for attach in parts:
            name, part = list(attach.items())[0]
            part["Content-Disposition"] = f'attachment; filename="{name}"'
            message.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, recipient, message.as_string())
        print(f"Message sent to {recipient}!")

class AutoMail:
    def __init__(self, template_path=None):
        self.template = Template(open(template_path).read())

    def generate_emails(self, mail_list_filename):
        with open(mail_list_filename) as file:
            mergemail_file = csv.DictReader(file)
            headers = mergemail_file.fieldnames
            for row in mergemail_file:
                yield row, headers

    def render_email(self, row, headers, context_variables):
        context = {}
        context.update(context_variables)
        context.update({header: row[header] for header in headers})
        return self.template.render(context)

class WebApp:
    def __init__(self, app, email_sender):
        self.app = app
        self.email_sender = email_sender
        self.context_variables = self.load_context_variables()

    def _fresh_load(self):
        for key in os.environ.keys():
            if 'ctx_' in key.lower():
                os.environ.pop(key)
        load_dotenv()

    def load_context_variables(self):
        self._fresh_load()
        context_vars = []
        for key, value in os.environ.items():
            if 'ctx_' in key.lower():
                ctx = {}
                key_splits = key.split('_')
                ctx['key'] = '_'.join(key_splits[2:]).lower()
                ctx['type'] = key_splits[1].lower()
                ctx['value'] = value
                context_vars.append(ctx)
        return context_vars

    def setup_routes(self):
        self.app.add_url_rule("/", view_func=self.index, methods=['GET', 'POST'])

    def index(self):
        if request.method == 'GET':
            return render_template('main.html', tiny_api=os.environ.get("TINY_API_KEY"), context_variables=self.context_variables)
        else:
            try:
                tmp_path = Path('.tmp')
                tmp_path.mkdir(parents=True, exist_ok=True)

                subject = request.form["subject"]
                body_file = request.files.get("body_file")
                body_file.save(f'.tmp/{body_file.filename}')
                body = request.form.get("body")
                attendance_criteria = request.form.get("attendance_criteria")
                mail_list = request.files.get("mail_list")
                mail_list.save('.tmp/mail_list.csv')
                attached_files = request.files.getlist('attachments')

                session["subject"] = subject
                session["body_filename"] = body_file.filename
                session["body"] = body

                if not subject or not mail_list.filename:
                    flash('You must specify all fields')
                    return redirect(url_for('index'))

                parts = []
                if attached_files:
                    for attached_file in attached_files:
                        part = MIMEApplication(attached_file.read())
                        parts.append({attached_file.filename: part})

                context_variables = self.parse_context_variables(request.form)
                auto_mail = AutoMail(f'.tmp/{body_file.filename}')
                emails = []

                for row, headers in auto_mail.generate_emails('.tmp/mail_list.csv'):
                    if attendance_criteria.lower() != 'all' and row['attendance'].lower() != attendance_criteria.lower():
                        continue
                    subject_replaced = self.replace_placeholders(subject, headers, row, context_variables)
                    email_body = auto_mail.render_email(row, headers, context_variables)
                    email = row['email']
                    recipient_name = f"{row['firstName']} {row['lastName']}"

                    try:
                        self.email_sender.send_email(subject_replaced, email_body, parts, email, recipient_name)
                        emails.append(email)
                    except Exception as e:
                        print(f'Error: {e}')

                return {'count': len(emails), 'emails': emails, "status": 200}, 200
            except Exception as e:
                print(format_exc())
                print(f'Short Error: {e}')
                return {'message': str(e), "status": 500}, 500
            finally:
                tmp_files = glob('.tmp/*')
                for f in tmp_files:
                    os.remove(f)
                os.rmdir('.tmp')
                print('Cleared temporary files!')

    @staticmethod
    def parse_context_variables(form):
        context_variables = {}
        context_names = [key for key in form.keys() if key.startswith('context_name_')]
        for name in context_names:
            index = name.split('_')[-1]
            context_name = form[name]
            context_type = form[f'context_type_{index}']
            context_value = form[f'context_value_{index}']
            if context_type == 'datetime':
                context_value = datetime.strftime(datetime.strptime(context_value, '%Y-%m-%dT%H:%M'), "%A, %B %d, %Y, %I:%M %p")
            context_variables[context_name] = context_value
        return context_variables

    @staticmethod
    def replace_placeholders(text, headers, row, context_variables):
        for header in headers:
            text = re.sub(f"{{{{\s*{header}\s*}}}}", row[header], text)
        for k, v in context_variables.items():
            text = re.sub(f"{{{{\s*{k}\s*}}}}", v, text)
        return text

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    sender = os.environ.get('FROM_MAIL')
    sender_name = os.environ.get('FROM_NAME')
    password = os.environ.get('APP_PASS')

    email_sender = EmailSender(sender, sender_name, password)
    web_app = WebApp(app, email_sender)
    web_app.setup_routes()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
