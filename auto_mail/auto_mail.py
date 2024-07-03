"""This module renders emails using Jinja2
"""
import csv
from typing import List, Dict, Generator, Tuple, Any, Sequence
from jinja2 import Template

class AutoMail:
    """
    Class for rendering emails using a Jinja2 template.
    """

    def __init__(self, template_path: str) -> None:
        """
        Initialize the AutoMail class.

        Args:
            template_path (str): The path to the Jinja2 template file.
        """
        with open(template_path, encoding='utf-8') as file:
            self.template = Template(file.read())

    def generate_email_fields(
            self, mail_list_filename: str
            ) -> Generator[Tuple[Dict[str | Any, str | Any], Sequence[str] | None], None, None]:
        """
        Generate email fields from a CSV file.

        Args:
            mail_list_filename (str): The path to the CSV file containing email fields.

        Yields:
            Tuple[Dict[str, str], List[str]]: A tuple containing a dictionary of email fields \
                per mail list instance and a list of field headers.
        """
        with open(mail_list_filename, encoding='utf-8') as file:
            mergemail_file = csv.DictReader(file)
            headers = mergemail_file.fieldnames
            for row in mergemail_file:
                yield row, headers

    def render_email(
            self, row: Dict[str, str], headers: List[str], context_variables: Dict[str, str]
            ) -> str:
        """
        Render the email body using the provided context variables and email fields.

        Args:
            row (Dict[str, str]): A dictionary containing email fields.
            headers (List[str]): A list of field headers.
            context_variables (Dict[str, str]): A dictionary of context variables.

        Returns:
            str: The rendered email body.
        """
        context = {}
        context.update(context_variables)
        context.update({header: row[header] for header in headers})
        return self.template.render(context)
