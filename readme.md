# Online Appointment Booking System API

This API, built using Django REST Framework (DRF), offers a robust and scalable solution for managing online appointment bookings. It provides functionality for scheduling appointments, managing users, and controlling time slots efficiently.

## Prerequisites
Before setting up the project, ensure that you have the following installed:

- Python 3.11
- Django 5.1 or higher
- Django REST Framework
- Virtualenv (optional but recommended)

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammd-1819/Online-Reservation-API.git


2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate


3. **Install the required dependencies:**
   ```bash
    pip install -r requirements.txt


4. **Apply the migrations:**
   ```bash
    python manage.py migrate


5. **Create a superuser for the admin panel (optional but recommended):**
   ```bash
    python manage.py createsuperuser
    default is: admin@gmail.com
    password : admin


6. **Run the development server:**
    ```bash
    python manage.py runserver


7. **Access the application:**
    Open your browser and go to http://127.0.0.1:8000/ for the main page


## Features
- User authentication using JWT token
- Reserve, view, and manage appointments.
- API to display available doctors for specific dates and times.
- Manage doctors, time slots, and appointments.

## Usage
Once the server is running, users can:

- Browse available time slots.
- Reserve appointments for desired doctors and times.
- Admins can manage users, doctors, and appointment slots via the admin interface.

## API Endpoints
- Authentication: access and refresh tokent for users
- Appointments: Create, view, update, and delete appointments.
- Doctors: Manage doctors and their availability.

## Technologies Used
- Backend: Django REST Framework
- Database: PostgreSQL
- Authentication: Customized Django built-in authentication system

## Authors
Developed by Mohammad Charipour
