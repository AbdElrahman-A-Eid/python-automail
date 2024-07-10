"""
Module for generating email templates using LangChain and LLMs.

This module provides a class `TemplateGenerator` that utilizes LangChain and
the AnyScale platform to generate email HTML templates with inline styling and
context variables using a language model.
"""

import json
from typing import Dict

from langchain_community.chat_models import ChatAnyscale

class TemplateGenerator:
    """
    A class to generate email templates using a language model from AnyScale platform.

    Attributes:
        system_prompt (str): The system prompt guiding the LLM to generate email content.
    """

    SYSTEM_PROMPT = """
    You are an advanced language model that helps users generate professional and good-looking email HTML template content. The email body should be nicely formatted (e.g., centered container (text other than title though shouldn't be centered but justified or aligned left as the template style requires) with colored sections if needed) with strictly inline CSS for styling (adjust styling to user request if instructed) and should utilize Jinja2 context variables wherever relevant. The output must be structured as a JSON object with two keys: 'subject' and 'body'.

    Guidelines:
    1. **Subject**: Generate a concise and relevant subject for the email.
    2. **Body**: Create an HTML body for the email with inline CSS styles only (No html or body tags needed). 
    3. **Context Variables**: Utilize the provided context variables using the Jinja2 format (e.g., {{{{ variable_name }}}}).

    Available context variables:
    {context_variables}

    The output must be strictly a JSON object with no surrounding text (REMOVE ANY TEXT OUTSIDE THE JSON OUTPUT IN YOUR RESPONSE) just like this:
    {{
        "subject": "Your subject here",
        "body": "Your HTML body here with inline styles and context variables (Should include the whole html code within a single string)"
    }}
    """

    def __init__(
            self, model_name="meta-llama/Meta-Llama-3-70B-Instruct",
            temperature=1, base_url='https://api.endpoints.anyscale.com/v1',
            max_output_length=4096, top_p=1, frequency_penalty=0
            ):
        """
        Initializes the EmailTemplateGenerator with the specified model and parameters.

        Args:
            model_name (str): The name of the model to use from AnyScale.
            temperature (float): The temperature setting for the LLM.
            base_url (str): The base URL for the AnyScale API.
        """
        self.llm = ChatAnyscale(
                model = model_name,
                base_url = base_url,
                temperature = temperature,
                max_tokens = max_output_length,
                top_p = top_p,
                frequency_penalty = frequency_penalty
            ).bind(response_format={"type": "json_object"})

    def generate_template(
                self, user_prompt, context_variables, system_prompt: str=""
            ) -> Dict[str,str]:
        """
        Generates an email template using the specified user prompt and context variables.

        Args:
            user_prompt (str): The prompt provided by the user to guide the LLM.
            context_variables (list): A list of context variables to include in the email.

        Returns:
            Dict[str, str]: A dictionary with 'subject' and 'body' keys containing \
                the generated email content.
        """
        if not system_prompt:
            system_prompt = self.SYSTEM_PROMPT

        context_variables_str = "\n".join([f"\t- {{ {var} }}" for var in context_variables])
        prompt = system_prompt.format(context_variables=context_variables_str)

        messages = [
            ("system", prompt),
            ("human", user_prompt)
        ]

        response = self.llm.invoke(messages)

        print(response)

        return json.loads(response.content)
