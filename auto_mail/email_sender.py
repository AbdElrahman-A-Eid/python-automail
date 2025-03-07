"""Module for sending emails using SMTP SSL
"""
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

class EmailSender:
    """
    Class for sending emails using SMTP SSL.
    """

    def __init__(self, sender: str, sender_name: str, password: str, num_processes: int) -> None:
        """
        Initialize the EmailSender class.

        Args:
            sender (str): The sender's email address.
            sender_name (str): The sender's display name.
            password (str): The sender's app password.
            num_processes (int): The number of parallel processes for sending emails.
        """
        self.sender = sender
        self.sender_name = sender_name
        self.password = password
        self.num_processes = num_processes

    def send_email(
        self,
        subject: str,
        body: str,
        parts: List[Dict[str, MIMEApplication]],
        recipient: str,
        recipient_name: str
    ) -> None:
        """
        Send an email using SMTP SSL.

        Args:
            subject (str): The email subject.
            body (str): The email body.
            parts (List[Dict[str, MIMEApplication]]): A list of dictionaries with filename as key \
                and MIMEApplication objects representing email attachments as values.
            recipient (str): The recipient's email address.
            recipient_name (str): The recipient's display name.
        """
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

    def send_emails_parallel(
        self,
        parts: List[Dict[str, MIMEApplication]],
        recipients: List[Dict[str, str]]
    ) -> None:
        """
        Send emails to multiple recipients in parallel.

        Args:
            parts (List[Dict[str, MIMEApplication]]): A list of dictionaries with filename as key \
                and MIMEApplication objects representing email attachments as values.
            recipients (List[Dict[str, str]]): A list of dictionaries with 'email', 'name', \
                'subject', and 'body' keys representing recipient's email addresses, display names,\
                    and personalized subject and content.
        """
        with ThreadPoolExecutor(max_workers=self.num_processes) as executor:
            futures = [
                executor.submit(
                    self.send_email,
                    recipient['subject'],
                    recipient['body'],
                    parts,
                    recipient['email'],
                    recipient['name']
                )
                for recipient in recipients
            ]
            for future in as_completed(futures):
                future.result()  # Wait for all futures to complete
