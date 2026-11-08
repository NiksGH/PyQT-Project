# Always-read

Always-read is a small desktop library catalog application built with Python, PyQt5, and SQLite. It was created as an educational project.

The application interface is currently in Russian.

## Features

- Sign in as a librarian or a reader.
- Browse books and authors.
- Search books by title and authors by name.
- View a book description and the titles associated with an author.
- Add books and authors and edit catalog information as a librarian.
- See whether a book is assigned to a reader.

The application does not implement a checkout or return workflow. Search is case-sensitive and searches only the book title or author name.

## Requirements

- Python 3.8 or later
- PyQt5 5.15.7 (installed from `requirements.txt`)

## Run the application

From the project directory, create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python Always_read.py
```

### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Always_read.py
```

On the first launch, create separate logins and passwords for a librarian and a reader. Passwords must contain at least eight characters. The application stores salted PBKDF2-HMAC-SHA256 password hashes in its local database; it does not ship default accounts.

The local SQLite file, `database.db`, is created beside `Always_read.py`. It is ignored by Git and starts with an empty catalog. Add authors and books after signing in as the librarian. Keep this local database private if you enter real reader or circulation data.

When upgrading from the original repository, back up any catalog data you need and remove the old `database.db` before launching this version. The old database schema stores passwords in plain text and is not compatible with the new password-hash schema.

## Project files

- `Always_read.py` — application UI, account setup, and SQLite operations.
- `requirements.txt` — runtime dependency for the library catalog application.
- `database.db` — generated locally on first run; not included in the repository.

## Security and limitations

This is an educational desktop application, not a production library system. Account setup and password hashing protect the local demo database, but the app has no account-management screen, password reset, automated backups, or checkout/return workflow. Permissions are primarily enforced by which controls the UI displays. Do not use it to store real personal data or as a security boundary.

The repository also contains Russian project and coursework documents. The README above describes the current application source; those documents may describe earlier design plans.
