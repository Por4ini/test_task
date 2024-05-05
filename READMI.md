
# Project Title

This is a Django Rest Api - test task project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python 3.11 on your machine. 

### Installing

Clone the repository to your local machine:

```bash
git clone https://github.com/Por4ini/test-task.git
```

Navigate to the project directory

Create virtual env:

```bash
python -m venv env
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

## Testing project 
Run the tests
```bash
python manage.py test
```

## Django Admin
For using Django Admin you need to create superuser:
```bash
python manage.py createsuperuser
```


### Running the Application Locally

To run the application, execute the following command in the project directory:

```bash
python manage.py runserver
```

### Django Admin
To access the Django Admin panel, navigate to:
```bash
http://localhost:8000/admin
```
##API Documentation
The API endpoints are documented in Swagger. Access the documentation by visiting:
```bash
http://localhost:8000/swagger/
```

##Docker Compose
To run the application using Docker Compose, follow these steps:
```bash
docker-compose build
docker-compose up
```
The application will be accessible at 
```bash
http://0.0.0.0:8000/
```
#Project Functionality

##Event Management
Create, read, update, and delete events.
Event registration for users.
##User Management
Custom user model for registration with email and password.
##Authentication
Basic user registration and authentication.
##Testing
Unit tests for API endpoints.

##Bonus Features
Containerized application with Docker.
Docker Compose for easy setup.
Advanced feature: event search or filtering.
Email notifications to users upon event registration.


##Contributors
[Sergio Porchini](https://github.com/Por4ini)