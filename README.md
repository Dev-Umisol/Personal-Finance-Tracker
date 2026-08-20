<a id="readme-top"></a>

<div align="center">

<h3 align="center">Personal Finance Tracker API</h3>

  <p align="center">
    A secured REST API built with FastAPI that allows users to register, authenticate via JWT, and manage personal financial transactions - with full ownership enforcement and persistent SQLite storage.
    <br />
    <a href="https://github.com/Dev-Umisol/Personal-Finance-Tracker"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Dev-Umisol/Personal-Finance-Tracker/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/Dev-Umisol/Personal-Finance-Tracker/issues/new?labels=enhancement">Request Feature</a>
  </p>

  <p align="center">
    <strong>Status:</strong> Complete
  </p>

</div>

<!-- BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" />
  <img src="https://img.shields.io/badge/Tested-pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" />
</p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about">About</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#api-endpoints">API Endpoints</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#security">Security</a></li>
    <li><a href="#running-tests">Running Tests</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT -->
## About

A production-style backend REST API for tracking personal income and expenses. Users register and authenticate with JWT tokens, and every transaction they create is privately scoped to their account, other users cannot view or delete it. Built to apply real-world backend development practices including ORM-based database access, secure password hashing, environment variable configuration, and layered application architecture.

*Solo backend project - applying FastAPI, SQLAlchemy, JWT authentication, and Pydantic in a production-style architecture.*

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

- **User Registration & Login** - secure account creation with `pwdlib` password hashing and JWT-based session tokens
- **JWT Authentication** - every protected endpoint requires a valid Bearer token; expired or invalid tokens return descriptive 401 errors
- **Transaction Management** - create, retrieve, and delete financial transactions tied to the authenticated user
- **Ownership Enforcement** - users can only delete their own transactions; attempts to delete another user's record return a 403 Forbidden response
- **Persistent Storage** - all users and transactions stored in SQLite via SQLAlchemy ORM with auto-created tables on startup
- **Environment Variable Security** - `SECRET_KEY` and `DATABASE_URL` loaded from `.env`, no secrets hardcoded anywhere in the codebase

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILT WITH -->
## Built With

| Layer              | Technology                          |
| ------------------ | ------------------------------------ |
| Framework          | FastAPI                              |
| ORM                | SQLAlchemy                           |
| Database           | SQLite                               |
| Authentication     | JWT (`PyJWT`), OAuth2 Password Flow  |
| Password Hashing   | `pwdlib`                             |
| Data Validation    | Pydantic v2                          |
| Config Management  | `python-dotenv`                      |
| Testing            | pytest                               |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.x
* pip

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Dev-Umisol/Personal-Finance-Tracker.git
   cd Personal-Finance-Tracker
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file
   ```sh
   echo "SECRET_KEY=your-secret-key-here" >> .env
   echo "DATABASE_URL=sqlite:///./finance.db" >> .env
   ```
4. Run the API
   ```sh
   uvicorn app.main:app --reload
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

Visit `http://localhost:8000/docs` for the interactive Swagger UI, where every endpoint can be tested directly in the browser.

```sh
# Register a user
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'

# Log in to get a JWT
curl -X POST http://localhost:8000/users/login \
  -d "username=you@example.com&password=yourpassword"

# Create a transaction (requires the token from login)
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 42.50, "description": "Groceries"}'
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- API ENDPOINTS -->
## API Endpoints

| Method   | Endpoint              | Auth Required | Description                                |
| -------- | --------------------- | :------------: | ------------------------------------------- |
| `POST`   | `/users/register`     | ❌             | Register a new user                         |
| `POST`   | `/users/login`        | ❌             | Login and receive a JWT access token        |
| `POST`   | `/transactions`       | ✅             | Create a new transaction                    |
| `GET`    | `/transactions`       | ✅             | Get all transactions for the current user   |
| `DELETE` | `/transactions/{id}`  | ✅             | Delete a transaction by ID (owner only)      |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ARCHITECTURE -->
## Architecture

The project follows a clean layered structure with clear separation of concerns:

```
app/
│
├── main.py          # FastAPI app, routes, JWT logic, auth dependency
├── crud.py          # All database operations (create, read, delete)
├── models.py        # SQLAlchemy ORM models (Users, Transactions)
├── schemas.py        # Pydantic request/response schemas
├── database.py       # Engine, session, and Base configuration
└── .env              # SECRET_KEY and DATABASE_URL (not committed)
```

- **`main.py`** handles routing and authentication middleware
- **`crud.py`** contains all database queries, keeping business logic out of routes
- **`models.py`** defines the database schema with a one-to-many relationship between Users and Transactions
- **`schemas.py`** separates request and response shapes using Pydantic, `UserCreate` vs `UserResponse`, `TransactionCreate` vs `TransactionResponse`
- **`database.py`** manages the SQLAlchemy engine and provides a `get_db()` dependency via `yield`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SECURITY -->
## Security

- Passwords are hashed using `pwdlib` with the recommended algorithm, plaintext passwords are never stored
- JWT tokens expire after 30 minutes and include `sub`, `exp`, and `action` claims
- `SECRET_KEY` is loaded from environment variables, the app raises a `ValueError` at startup if it is missing
- Ownership checks on delete prevent users from deleting each other's transactions

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- RUNNING TESTS -->
## Running Tests

```sh
pytest Tests/
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Add transaction categories (Food, Rent, Income, etc.) for spending breakdowns
- [ ] Add a `GET /transactions/summary` endpoint returning total income, expenses, and balance
- [ ] Migrate from SQLite to PostgreSQL for production readiness
- [ ] Add a token refresh endpoint so users don't need to re-login every 30 minutes
- [ ] Containerize with Docker for portable deployment

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Destin Nguyen - [Portfolio](https://devdestinportfolio.vercel.app) - [GitHub](https://github.com/Dev-Umisol)

Project Link: [https://github.com/Dev-Umisol/Personal-Finance-Tracker](https://github.com/Dev-Umisol/Personal-Finance-Tracker)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
