"""This module manages the web application
"""
import os
import re
from json.decoder import JSONDecodeError
from datetime import datetime
from email.mime.application import MIMEApplication
from glob import glob
from pathlib import Path
from smtplib import SMTPConnectError
from traceback import format_exc
from typing import Dict, List, Any

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from langchain_core.exceptions import LangChainException

from auto_mail.auto_mail import AutoMail
from auto_mail.email_sender import EmailSender
from auto_mail.template_generator import TemplateGenerator


class WebApp:
    """
    Class for managing the web application.
    """

    def __init__(self, flask_app: Flask, email_sender: EmailSender) -> None:
        """
        Initialize the WebApp class.

        Args:
            flask_app (Flask): The Flask application instance.
            email_sender (EmailSender): An instance of the EmailSender class.
        """
        self.app = flask_app
        self.email_sender = email_sender
        self.context_variables = self.load_context_variables()

    def _fresh_load(self) -> None:
        """
        Reload environment variables from the .env file.
        """
        for key in os.environ:
            if 'pyauto_ctx_' in key.lower():
                os.environ.pop(key)
        load_dotenv()

    def load_context_variables(self) -> List[Dict[str, str]]:
        """
        Load context variables from environment variables.

        Returns:
            List[Dict[str, str]]: A list of context variable dictionaries.
        """
        self._fresh_load()
        context_vars = []
        print("Loading Permenant Context Variables:")
        for key, value in os.environ.items():
            if 'pyauto_ctx_' in key.lower():
                print(key, value)
                ctx = {}
                key_splits = key.split('_')
                ctx['key'] = '_'.join(key_splits[3:]).lower()
                ctx['type'] = key_splits[2].lower()
                ctx['value'] = value
                context_vars.append(ctx)
        return context_vars

    def setup_routes(self) -> None:
        """
        Setup the URL routes for the Flask application.
        """
        self.app.add_url_rule("/", view_func=self.index, methods=['GET', 'POST'])
        self.app.add_url_rule("/generate", view_func=self.generate, methods=['POST'])

    def index(self):
        """
        Handle the index route for rendering and processing the email form.

        Returns:
            The rendered template or a JSON response.
        """
        if request.method == 'GET':
            return render_template(
                'index.html', 
                tiny_api=os.environ.get("TINY_API_KEY"),
                context_variables=self.context_variables
            )
        else:
            try:
                tmp_path = Path('.tmp')
                tmp_path.mkdir(parents=True, exist_ok=True)

                subject = request.form["subject"]
                body_file = request.files.get("body_file")
                body_file.save(f'.tmp/{body_file.filename}')
                attendance_criteria = request.form.get("attendance_criteria")
                progress_criteria = request.form.get("progress_criteria")
                mail_list = request.files.get("mail_list")
                mail_list.save('.tmp/mail_list.csv')
                attached_files = request.files.getlist('attachments')

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
                recipients = []

                for row, headers in auto_mail.generate_email_fields('.tmp/mail_list.csv'):
                    attendance_condition = ('attendance' in headers
                                    and attendance_criteria.lower() != 'all'
                                    and row['attendance'].lower() != attendance_criteria.lower())
                    progress_condition = ('progress' in headers
                                    and progress_criteria.lower() != 'all'
                                    and row['progress'].lower() != progress_criteria.lower())
                    if attendance_condition or progress_condition:
                        continue
                    subject_replaced = self.replace_placeholders(
                        subject, headers, row, context_variables
                    )
                    email_body = auto_mail.render_email(row, headers, context_variables)
                    email = row['email']
                    recipient_name = f"{row['firstName']} {row['lastName']}"

                    try:
                        if self.email_sender.num_processes > 1:
                            recipients.append({
                                'name': recipient_name,'email': email, 
                                'subject': subject_replaced, 'body': email_body
                                })
                        else:
                            self.email_sender.send_email(
                                subject_replaced, email_body, parts, email, recipient_name
                            )
                        emails.append(email)
                    except (SMTPConnectError, TimeoutError) as e:
                        print(f'Error: {e}')

                if recipients:
                    try:
                        self.email_sender.send_emails_parallel(
                                parts, recipients
                            )
                    except (SMTPConnectError, TimeoutError) as e:
                        print(f'Error: {e}')

                print(f"Number of total emails sent is {len(emails)}!")
                return {'count': len(emails), 'emails': emails, "status": 200}, 200
            except (RuntimeError, ValueError, TypeError, LookupError, OSError) as e:
                print(format_exc())
                print(f'Short Error: {e}')
                return {'message': str(e), "status": 500}, 500
            finally:
                tmp_files = glob('.tmp/*')
                for f in tmp_files:
                    os.remove(f)
                os.rmdir('.tmp')
                print('Cleared temporary files!')

    def generate(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        if not os.environ.get("ANYSCALE_API_KEY", ""):
            return {
                "message": "Cannot find a proper ANYSCALE_API_KEY variable in .env file!",
                "status": 500
                }, 500

        params: Dict[str, Any] = request.get_json()

        user_prompt = params.pop("user_prompt")
        if not user_prompt.strip():
            return {
                "message": "Prompt cannot be empty!",
                "status": 500
                }, 500

        system_prompt = params.pop("system_prompt")

        context_variables = params.pop("context_variables")

        try:
            generator = TemplateGenerator(
                    model_name = params.pop("model"),
                    **params
                )
            template, metadata =  generator.generate_template(
                user_prompt, context_variables, system_prompt
            )
        except (RuntimeError, LangChainException, JSONDecodeError) as e:
            return {
                "message": e,
                "status": 500
                }, 500


        return {'template': template, 'metadata': metadata,
                'status': 200}, 200

    @staticmethod
    def parse_context_variables(form: Dict[str, str]) -> Dict[str, str]:
        """
        Parse context variables from the form data.

        Args:
            form (Dict[str, str]): The form data.

        Returns:
            Dict[str, str]: A dictionary of context variables.
        """
        context_variables = {}
        context_names = [key for key in form.keys() if key.startswith('context_name_')]
        for name in context_names:
            index = name.split('_')[-1]
            context_name = form[name]
            context_type = form[f'context_type_{index}']
            context_value = form[f'context_value_{index}']
            if context_type == 'datetime':
                context_value = datetime.strftime(
                    datetime.strptime(context_value, '%Y-%m-%dT%H:%M'),
                    "%A, %B %d, %Y, %I:%M %p"
                )
            context_variables[context_name] = context_value
        return context_variables

    @staticmethod
    def replace_placeholders(
        text: str, headers: List[str], row: Dict[str, str], context_variables: Dict[str, str]
        ) -> str:
        """
        Replace placeholders in the text with values from headers and context variables.

        Args:
            text (str): The text with placeholders.
            headers (List[str]): The list of field headers.
            row (Dict[str, str]): The dictionary of email fields.
            context_variables (Dict[str, str]): The dictionary of context variables.

        Returns:
            str: The text with placeholders replaced.
        """
        for header in headers:
            text = re.sub(rf"{{{{\s*{header}\s*}}}}", row[header], text)
        for k, v in context_variables.items():
            text = re.sub(rf"{{{{\s*{k}\s*}}}}", v, text)
        return text
