# KanMind

KanMind is the REST backend of a Kanban board, built with Django and Django REST Framework as a project of a full-stack web development course. Users register and log in with their e-mail address, create boards with members, manage tasks with an assignee and a reviewer, and comment on tasks. The API uses token authentication and stores its data in SQLite. The frontend is not part of this repository.

## Quickstart

### Prerequisites

- Python 3.12 or newer (required by Django 6.1), developed with Python 3.15.0
- Git

### Setup

Clone the repository, create a virtual environment, install the dependencies and create the `.env` file.

Windows (PowerShell):

```powershell
git clone https://github.com/AnneManthey/KanMind.git
cd KanMind
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.template .env
```

macOS / Linux:

```bash
git clone https://github.com/AnneManthey/KanMind.git
cd KanMind
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.template .env
```

Generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Open `.env` and replace `YOUR-SECRET-KEY` with the generated value. Keep the quotes around it.

Create the database, create an admin user and start the server. `createsuperuser` asks for e-mail, full name and password.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/`

## Usage

### Authentication

Registration and login are open and return a token:

```http
POST /api/registration/
Content-Type: application/json

{
  "fullname": "Example User",
  "email": "user@example.com",
  "password": "<your password>",
  "repeated_password": "<your password>"
}
```

`POST /api/login/` expects `email` and `password`. Every other endpoint needs this header:

```http
Authorization: Token <your token>
```

### Endpoints

| Method | Path | Purpose | Access |
|---|---|---|---|
| POST | `/api/registration/` | Create a user | open |
| POST | `/api/login/` | Log in | open |
| GET | `/api/boards/` | List own boards and memberships | logged in |
| POST | `/api/boards/` | Create a board (`title`, `members`) | logged in |
| GET | `/api/boards/{board_id}/` | Board with members and tasks | owner or member |
| PATCH | `/api/boards/{board_id}/` | Change title and members | owner or member |
| DELETE | `/api/boards/{board_id}/` | Delete a board | owner |
| GET | `/api/email-check/?email=` | Find a user by e-mail | logged in |
| GET | `/api/tasks/assigned-to-me/` | Tasks assigned to you | logged in |
| GET | `/api/tasks/reviewing/` | Tasks you review | logged in |
| POST | `/api/tasks/` | Create a task | board owner or member |
| PATCH | `/api/tasks/{task_id}/` | Update a task | board owner or member |
| DELETE | `/api/tasks/{task_id}/` | Delete a task | task creator or board owner |
| GET | `/api/tasks/{task_id}/comments/` | List comments, oldest first | board owner or member |
| POST | `/api/tasks/{task_id}/comments/` | Add a comment (`content`) | board owner or member |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` | Delete a comment | comment author |

Task fields for writing: `board`, `title`, `description`, `status`, `priority`, `assignee_id`, `reviewer_id`, `due_date`.

- `status`: `to-do` (default), `in-progress`, `review`, `done`
- `priority`: `low`, `medium` (default), `high`

## Notes

- Users log in with their e-mail address, there is no username. Registration and e-mail check ignore upper and lower case, login expects the spelling used at registration.
- The board owner is not added to `members` automatically. Access is granted to the owner and to all members.
- Assignee and reviewer must belong to the board. The board of a task cannot be changed.
- The responses of board and task `PATCH` differ from the `GET` responses, as specified by the course API documentation.
- Password strength validators are not applied at registration.
- CORS allows `http://127.0.0.1:5500` and `http://localhost:5500` (VS Code Live Server). Add other frontend origins to `CORS_ALLOWED_ORIGINS` in `core/settings.py`.
- The settings are meant for local development (`DEBUG=True`, SQLite). Do not use them in production.
- `.env` holds the secret key and is excluded from Git.
