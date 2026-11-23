# KanMind

KanMind is a Django backend in development for an Angular-based Kanban board. It provides the foundation for the board's server-side functionality. The project currently includes Django's admin route and is configured to use SQLite for local development.

## Quickstart

### Prerequisites

- Python 3.12 or newer

### Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy the environment template to `.env` in the project root, then replace its `SECRET_KEY` placeholder as described below. Initialize the database and start Django:

```powershell
Copy-Item .env.template .env
python manage.py migrate
python manage.py runserver
```

The development server is available at `http://127.0.0.1:8000/`. The configured admin route is `http://127.0.0.1:8000/admin/`.

## Secret key

Django reads `SECRET_KEY` from the root `.env` file via `python-dotenv`. The tracked `.env.template` contains a placeholder; generate a key with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace the placeholder in `.env` with the generated value:

```dotenv
SECRET_KEY=replace_with_your_generated_key
```

Keep the key private and do not commit `.env`; it is excluded by `.gitignore`. Use a separate secret key for each environment.

## Notes

- The project is configured for local development (`DEBUG=True`) and SQLite. Do not use the current settings as-is for production.
- The URL configuration currently exposes only Django's admin; application API endpoints are not configured yet.
