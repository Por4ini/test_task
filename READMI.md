Python (Django Rest Framework) Test Task

This project is a Django-based REST API for Event Management. It allows users to create, view, update, and delete events, as well as handle user registrations for these events. The API documentation is available in Swagger.


Installation

Clone the repository:

git clone https://github.com/your_username/your_project.git

Navigate to the project directory:

cd your_project

Install dependencies:

pip install -r requirements.txt

Run migrations:
python manage.py migrate

Create admin:
python manage.py createsuperuser

Start the development server:
python manage.py runserver

API Documentation

The API endpoints are documented in Swagger. Access the documentation by running the server and visiting the following URL in your browser:


http://localhost:8000/swagger/

Key Features

Event Management:
Create, Read, Update, Delete events.
Event registration for users.
User Management:
Custom user model with email and password.
Authentication:
Basic User Registration and Authentication.
Testing:
Unit tests for API endpoints.

Bonus Features

Docker:
Containerized application with Docker.
Docker Compose for easy setup.
Advanced Features:
Event search or filtering.
Email Notifications:
Send email notifications to users upon event registration.
Contributors

https://github.com/Por4ini