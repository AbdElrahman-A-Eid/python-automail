<img src="static/img/logo.png" alt="Python AutoMail App Logo" width=150 style="display: block; margin-left: auto; margin-right: auto; margin-bottom: 15px;"/>

# Python Auto Mail

Python Auto Mail is an automated email template generation and sending application designed to streamline and personalize your email communication process. This project combines a web interface for user input and configuration with backend functionality to generate and send dynamic, personalized emails efficiently.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Setting Up the Environment](#setting-up-the-environment)
5. [Usage](#usage)
6. [Features](#features)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

---

## Introduction

Python Auto Mail provides a user-friendly interface for generating and sending customized emails. It leverages advanced language models to generate high-quality email content, supports HTML templates with Jinja2 for dynamic content, and allows for easy configuration of various parameters to suit your needs. With Python Auto Mail, you can enhance your email marketing, communication, and engagement strategies effortlessly.


---

## Project Structure

```
.
├── auto_mail
│   ├── __init__.py
│   ├── auto_mail.py
│   ├── email_sender.py
│   ├── template_generator.py
│   └── web_app.py
├── static
│   ├── css
│   │   └── styles.css
│   ├── img
│   │   ├── favicon.ico
│   │   └── logo.png
│   └── js
│       ├── context-variable.js
│       ├── form.js
│       ├── notification.js
│       ├── sidebar.js
│       └── tinymce-init.js
├── templates
│   ├── index.html
│   └── examples
│       ├── generated_1.html
│       ├── generated_2.html
│       ├── generated_3.html
│       ├── generated_4.html
│       └── generated_5.html
├── .env.template
├── .gitignore
├── app.py
└── requirements.txt
```

---

## Installation

To get started with Python Auto Mail, follow the steps below to set up the project on your local machine.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tools (optional but recommended)

### Steps

1. **Clone the repository**

    ```bash
    git clone https://github.com/AbdElrahman-A-Eid/python-automail.git
    cd auto_mail
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv automail_env
    source automail_env/bin/activate  # On Windows use `automail_env\Scripts\activate`
    ```

3. **Install the required packages**

    ```bash
    pip install -r requirements.txt
    ```

---

## Setting Up the Environment

Python Auto Mail uses environment variables for configuration. Follow the steps below to set up your `.env` file.

1. **Create a `.env` file**

    Copy the `.env.template` to `.env` and fill in the required values.

    ```bash
    cp .env.template .env
    ```

2. **Configure environment variables**

    Open the `.env` file in a text editor and provide the necessary configuration values. The `.env.template` includes placeholders for all required variables.

---

## Usage

After setting up the environment, you can start the Python Auto Mail application.

1. **Run the application**

    ```bash
    python app.py
    ```

2. **Access the web interface**

    Open your web browser and go to `http://127.0.0.1:5000` to access the Python Auto Mail web interface.

3. **Generate and send emails**

    Use the web interface to configure your email template and context variables, generate content, and send emails.

---

## Features

- **Personalized Email Sending**: Easily send personalized and dynamic emails to multiple addresses.
- **HTML Templates with Jinja2 Support**: Use HTML templates with Jinja2 for dynamic content inclusion.
- **Context Variables**: Define context variables to customize email content dynamically.
- **Attachments**: Add attachments to your emails.
- **Email Template Generation**: Generate email templates using various language models with adjustable parameters.
- **Customizable Parameters**: Adjust parameters like temperature, max output length, top-p, and frequency penalty for template generation.
- **Web Interface**: User-friendly web interface for configuration and email management.
- **Email Sending**: Integrated functionality to send emails directly from the application.

---


## Contributing

Contributions are welcome! If you'd like to contribute to Python Auto Mail, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and make sure they are well-documented.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request adding detailed description and documentation on your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
