# User Authentication API

A FastAPI-based User Authentication API with JWT authentication, OTP verification, profile management, and standardized API responses.

## Features

* User signup
* OTP generation and verification
* User login
* JWT access and refresh tokens
* User profile
* Logout / refresh-token handling
* Standardized API response format using `status`, `data`, and `error`
* PostgreSQL database integration
* Environment-based configuration

## Tech Stack

* Python
* FastAPI
* Uvicorn
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT
* Python-dotenv

## Project Structure

```text
user-auth-practice/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── otp.py
│   │       └── profile.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── otp.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── common.py
│   │   ├── otp.py
│   │   └── user.py
│   │
│   └── services/
│       ├── auth_service.py
│       ├── otp_service.py
│       └── user_service.py
│
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Environment Setup

Create a `.env` file in the project root and provide the required configuration values.

The required environment variables are:

```env
DATABASE_URL=
JWT_SECRET_KEY=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
OTP_EXPIRE_MINUTES=5
OTP_LENGTH=6
```

Do not commit the `.env` file to GitHub because it may contain sensitive credentials and secrets.

## Installation

Clone the repository and move into the project directory.

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI application using Uvicorn:

```powershell
uvicorn main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the authentication endpoints.

## Main Endpoints

| Method | Endpoint             | Purpose                          |
| ------ | -------------------- | -------------------------------- |
| POST   | `/auth/signup`       | Register a new user              |
| POST   | `/auth/generate-otp` | Generate OTP                     |
| POST   | `/auth/verify-otp`   | Verify OTP                       |
| POST   | `/auth/login`        | Login and generate JWT tokens    |
| GET    | `/profile`           | Get authenticated user's profile |

## Response Format

The API uses a standardized response wrapper.

### Successful response

```json
{
  "status": true,
  "data": {},
  "error": null
}
```

### Error response

```json
{
  "status": false,
  "data": null,
  "error": {
    "code": 400,
    "msg": "Error message"
  }
}
```

## Authentication

Protected endpoints require a valid JWT access token.

In Swagger UI, use the **Authorize** button and provide the access token to access protected endpoints.

## Notes

* Keep `.env` private.
* Do not commit passwords, database credentials, JWT secrets, or other sensitive information.
* Use `.env.example` as a template for required environment variables.
