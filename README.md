# Personal Finance Tracker API

> A secured REST API built with FastAPI that allows users to register, authenticate via JWT, and manage personal financial transactions — with full ownership enforcement and persistent SQLite storage.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![pytest](https://img.shields.io/badge/Tested-pytest-0A9EDC?logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## About

A production-style backend REST API for tracking personal income and expenses. Users register and authenticate with JWT tokens, and every transaction they create is privately scoped to their account, other users cannot view or delete it. Built to apply real-world backend development practices including ORM-based database access, secure password hashing, environment variable configuration, and layered application architecture.

---

## Features

- **User Registration & Login** - Secure account creation with `pwdlib` password hashing and JWT-based session tokens
- **JWT Authentication** - Every protected endpoint requires a valid Bearer token; expired or invalid tokens return descriptive 401 errors
- **Transaction Management** - Create, retrieve, and delete financial transactions tied to the authenticated user
- **Ownership Enforcement** - Users can only delete their own transactions; attempts to delete another user's record return a 403 Forbidden response
- **Persistent Storage** - All users and transactions stored in SQLite via SQLAlchemy ORM with auto-created tables on startup
- **Environment Variable Security** - `SECRET_KEY` and `DATABASE_URL` loaded from `.env`, no secrets hardcoded anywhere in the codebase

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite |
| Authentication | JWT (`PyJWT`), OAuth2 Password Flow |
| Password Hashing | `pwdlib` |
| Data Validation | Pydantic v2 |
| Config Management | `python-dotenv` |
| Testing | pytest |

---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `POST` | `/users/register` | ❌ | Register a new user |
| `POST` | `/users/login` | ❌ | Login and receive a JWT access token |
| `POST` | `/transactions` | ✅ | Create a new transaction |
| `GET` | `/transactions` | ✅ | Get all transactions for the current user |
| `DELETE` | `/transactions/{id}` | ✅ | Delete a transaction by ID (owner only) |

---

## Architecture

The project follows a clean layered structure with clear separation of concerns:

```
app/
│
├── main.py          # FastAPI app, routes, JWT logic, auth dependency
├── crud.py          # All database operations (create, read, delete)
├── models.py        # SQLAlchemy ORM models (Users, Transactions)
├── schemas.py       # Pydantic request/response schemas
├── database.py      # Engine, session, and Base configuration
└── .env             # SECRET_KEY and DATABASE_URL (not committed)
```

- **`main.py`** handles routing and authentication middleware
- **`crud.py`** contains all database queries, keeping business logic out of routes
- **`models.py`** defines the database schema with a one-to-many relationship between Users and Transactions
- **`schemas.py`** separates request and response shapes using Pydantic — `UserCreate` vs `UserResponse`, `TransactionCreate` vs `TransactionResponse`
- **`database.py`** manages the SQLAlchemy engine and provides a `get_db()` dependency via `yield`

---

## Security

- Passwords are hashed using `pwdlib` with the recommended algorithm — plaintext passwords are never stored
- JWT tokens expire after 30 minutes and include `sub`, `exp`, and `action` claims
- `SECRET_KEY` is loaded from environment variables — the app raises a `ValueError` at startup if it is missing
- Ownership checks on delete prevent users from deleting each other's transactions

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Dev-Umisol/Personal-Finance-Tracker.git
cd PersonalFinanceTracker

# Install dependencies
pip install -r requirements.txt

# Create a .env file
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "DATABASE_URL=sqlite:///./finance.db" >> .env

# Run the API
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Running Tests

```bash
pytest Tests/
```

---

## Future Improvements

- [ ] Add transaction categories (Food, Rent, Income, etc.) for spending breakdowns
- [ ] Add a `GET /transactions/summary` endpoint returning total income, expenses, and balance
- [ ] Migrate from SQLite to PostgreSQL for production readiness
- [ ] Add token refresh endpoint so users don't need to re-login every 30 minutes
- [ ] Containerize with Docker for portable deployment

---

*Solo backend project - applying FastAPI, SQLAlchemy, JWT authentication, and Pydantic in a production-style architecture 🐍*
