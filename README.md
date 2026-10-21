#Workout Tracker API

A RESTful Flask backend application designed to log and manage workout sessions, exercise libraries, and performance metrics. Built using Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

---

## Table of Contents
- [Overview](#-overview)
- [Project Architecture](#-project-architecture)
- [Requirements](#-requirements)
- [Installation & Setup](#-installation--setup)
- [Database Setup](#-database-setup)
- [Running the Server](#-running-the-server)
- [API Endpoints](#-api-endpoints)
- [Testing with Postman](#-testing-with-postman)

---

##  Overview

The Workout Tracker API allows users to:
1. Create and manage individual workout sessions.
2. Maintain a catalog of exercises categorized by muscle group and equipment needs.
3. Link exercises to workout sessions with detailed performance data (reps, sets, and duration).
4. Receive validation responses and error handling for invalid input data.

---

##  Project Architecture

```text
flask-workout-app/
├── Pipfile
├── Pipfile.lock
├── README.md
└── server/
    ├── app.py          # Flask application routes and configuration
    ├── app.db          # SQLite database file
    ├── models.py       # SQLAlchemy database models
    ├── schemas.py      # Marshmallow serialization & validation schemas
    ├── seed.py         # Database seed script
    └── migrations/     # Alembic migration files
```

---

##  Requirements

- **Python**: `^3.10`
- **Pipenv**: Virtual environment manager
- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migration handling
- **Marshmallow-SQLAlchemy**: Data serialization and validation

---

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd flask-workout-app
   ```

2. **Install project dependencies:**
   ```bash
   pipenv install
   ```

---

##  Database Setup

Run all setup commands from the root directory (`flask-workout-app`):

1. **Apply migrations to build database tables:**
   ```bash
   FLASK_APP=server/app.py pipenv run flask db upgrade head
   ```

2. **Seed the database with sample data:**
   ```bash
   PYTHONPATH=server pipenv run python server/seed.py
   ```

---

##  Running the Server

Start the local development server:

```bash
PYTHONPATH=server pipenv run python server/app.py
```

The server will start at: `http://127.0.0.1:5555`

---

##  API Endpoints

### 1. Workouts

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/workouts` | Retrieve all workouts |
| `GET` | `/workouts/<id>` | Retrieve a specific workout with nested exercises |
| `POST` | `/workouts` | Create a new workout session |
| `DELETE` | `/workouts/<id>` | Delete a workout session |

### 2. Exercises

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/exercises` | Retrieve all exercises |
| `GET` | `/exercises/<id>` | Retrieve a specific exercise |
| `POST` | `/exercises` | Create a new exercise entry |
| `DELETE` | `/exercises/<id>` | Delete an exercise |

### 3. Workout Exercises (Join Model)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Link an exercise to a workout |

---

## 🧪 Testing with Postman

### Example: Create a New Workout
* **Method:** `POST`
* **URL:** `http://127.0.0.1:5555/workouts`
* **Headers:** `Content-Type: application/json`
* **Body (raw JSON):**
  ```json
  {
    "date": "2026-10-25",
    "duration_minutes": 45,
    "notes": "Morning leg session"
  }
  ```

### Example: Link Exercise to Workout
* **Method:** `POST`
* **URL:** `http://127.0.0.1:5555/workouts/1/exercises/2/workout_exercises`
* **Headers:** `Content-Type: application/json`
* **Body (raw JSON):**
  ```json
  {
    "reps": 12,
    "sets": 4,
    "duration_seconds": 0
  }
  ```