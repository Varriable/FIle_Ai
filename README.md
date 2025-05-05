# File AI Management System

The **File AI Management System** is an advanced file management solution enhanced with artificial intelligence. This system allows users to interact with an AI while accessing and managing selected files, making file operations more intuitive and efficient.

## Features

- **AI Interaction**: Seamlessly interact with an AI model for enhanced file management.
- **Multiple Models**: Includes two distinct models, with `model1` being the most refined and user-friendly.
- **Admin Panel**: Manage and monitor operations through a built-in admin interface.
- **Database Integration**: Includes database migration capabilities for streamlined data handling.

## Requirements

To run the File AI Management System, you will need:

- **Pipenv**: For managing the virtual environment.
- **Local LLM**: A locally running language model via LM Studio.

## Getting Started

Follow these steps to set up and run the application:

1. **Activate the Virtual Environment**:
   ```bash
   pipenv shell
   ```

2. **Install Dependencies**:
   ```bash
   pipenv install
   ```

3. **Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the Application**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Admin Panel**:
   Navigate to `/admin` in your browser.

## Models

- **Model 1**: The primary model, designed for ease of use and refined functionality.
- **Model 2**: An alternative implementation for exploration and comparison.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to suggest features or report bugs.
