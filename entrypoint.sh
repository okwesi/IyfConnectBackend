#!/bin/bash
# Entry script for Docker container

# Run Django makemigrations
python manage.py makemigrations

# Run Django migrate
python manage.py migrate


# Start the Django development server
python manage.py runserver 0.0.0.0:8000
