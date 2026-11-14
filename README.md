# Job Application Tracker

A small Django app for tracking internship and job applications. Each user has a private list of applications that move through statuses (wishlist, applied, interview, offer, rejected).

## Features

- Sign up, log in and log out (Django's built-in auth)
- Create, edit and delete applications (class-based views)
- Per-user data isolation: users can only see and change their own records
- Search by company or position, filter by status, pagination
- Dashboard counts per status from a single aggregate query
- Django admin integration
- Automated tests for auth, isolation, filtering and stats

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations tracker
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign up.

## Run the tests

```bash
python manage.py test
```

## Project layout

```
config/     project settings and root URLs
tracker/    the app: models, forms, views, urls, admin, tests
templates/  base layout, auth pages and tracker pages
```

## Design notes

- `UserApplicationsMixin` scopes every queryset to `request.user`, so another user's record returns a 404 instead of leaking.
- Status values use `TextChoices`, which keeps the allowed values in one place for the model, form and filter.
- Settings read the secret key and debug flag from environment variables so nothing sensitive needs to be committed.

## Ideas for extending it

- Add an interview/follow-up date field and a reminders view
- CSV export
- Deploy to Render or Railway with PostgreSQL
- REST API with Django REST Framework
