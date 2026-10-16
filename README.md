### INF601 - Advanced Programming in Python
### Ray Bednara
### Mini Project 5


# Golf Scores

A Flask web app for saving post-round golf scores for yourself and up to
three friends, built on the application-factory/blueprint structure from the
official Flask tutorial.

## Description

This project implements `flaskr`, a Flask package with session-based
registration/login and a small golf-scoring workflow backed by SQLite:

* `flaskr/__init__.py` — the `create_app()` application factory that wires
  together config, the database, and both blueprints.
* `flaskr/db.py` — per-request SQLite connection handling (`get_db`/`close_db`)
  and the `flask init-db` CLI command that (re)builds the schema.
* `flaskr/schema.sql` — three tables: `users`, `rounds` (FK to `users`), and
  `players` (FK to `rounds`) — one `players` row per person per round.
* `flaskr/auth.py` — the `auth` blueprint: `register` (with password
  requirements — 8+ characters, upper/lowercase, a digit), `login`, `logout`,
  and the `login_required` decorator.
* `flaskr/scores.py` — the `scores` blueprint: a rounds dashboard (`index`),
  a GET/POST form to log a round and its players (`create`), a round detail
  page (`view`), and `delete`.
* `flaskr/templates/` — six pages (landing, register, login, dashboard,
  log-a-round form, round detail), all extending one `base.html` layout
  that pulls in Bootstrap 5 and includes a delete-confirmation modal.
* `query_db.py` — a standalone helper to peek at the SQLite tables from the
  command line while the dev server is running.

## Getting Started

### Dependencies

* Windows 10/11
* Python 3.13
* Flask (installed from `requirements.txt`; pulls in Werkzeug/Jinja2)
* Install required libraries with:
```
pip install -r requirements.txt
```

### Installing

* Clone or download this repository
* Create and activate a virtual environment, then install dependencies:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
* No file/folder modifications are needed; the SQLite database is created
  automatically inside `instance/` the first time it's initialized.

### Executing program

* Initialize the database (run once, or any time you want to reset it):
```powershell
$env:FLASK_APP = "flaskr"
flask init-db
```
* Start the dev server:
```powershell
flask run --debug
```
* Then visit http://127.0.0.1:5000/ in a browser:
    * Register an account (password must be 8+ characters with an uppercase
      letter, a lowercase letter, and a digit)
    * Log in
    * Click "Log a Round" to save a course, date, your score, and up to 3
      friends' names/scores
    * View "My Rounds" to see your history, open any round's detail page, or
      delete a round (confirmed via a Bootstrap modal)
* To inspect the database directly while the server is running, open a
  second terminal in the project root and run:
```powershell
python query_db.py
```

## Help

Running in Git Bash instead of PowerShell? Use the Bash equivalents for
activating the venv and setting the environment variable:
```bash
source venv/Scripts/activate
export FLASK_APP=flaskr
```

`flask run --debug` enables Werkzeug's auto-reloader, which runs the server
as a parent/child process pair so it can restart on code changes. On Windows,
Ctrl+C sometimes only stops the parent, leaving the child bound to port 5000.
Run `flask run --no-reload` instead if you want Ctrl+C to reliably kill the
server in one process, or force-free the port with:
```powershell
Get-NetTCPConnection -LocalPort 5000 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

## Authors

Ray Bednara
ray.bednara@gmail.com

## AI Usage

I used Claude Code to scaffold the whole project — the `flaskr` package
structure, the SQLite schema (`users` → `rounds` → `players`, linked by
foreign keys), the `auth` and `scores` blueprints, and all six Bootstrap-based
templates including the delete-confirmation modal. It ran the app end-to-end
(register, login, save a round, view the dashboard) to verify the flow
actually worked and to check the data landed correctly in SQLite, and caught
a real bug in the process — `schema.sql` originally dropped parent tables
before child tables, which fails under `PRAGMA foreign_keys = ON`. I also had
it add the password-strength validation on registration, and asked it
follow-up questions about Windows-specific quirks (PowerShell vs. Git Bash
setup commands, why Ctrl+C sometimes leaves the dev server's reloader child
process running on port 5000) and some general questions about how a project
like this would translate to a mobile app.
