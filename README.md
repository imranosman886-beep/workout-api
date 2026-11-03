# Workout Tracking API

## Project Description

This is a Flask REST API for tracking workouts and exercises. It allows users to create, view, and delete workouts and exercises, as well as add exercises to workouts.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Marshmallow
- SQLite
- Flask-Migrate

## Database Models

The project has three models:

- **Workout:** Stores the workout date, duration, and notes.
- **Exercise:** Stores the exercise name, category, and whether equipment is needed.
- **WorkoutExercise:** Connects workouts and exercises and stores reps, sets, and duration.

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | Get all workouts |
| GET | `/workouts/<id>` | Get one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| GET | `/exercises` | Get all exercises |
| GET | `/exercises/<id>` | Get one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises

| Method | Endpoint | Description |
|---|---|---|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Installation

1. Clone the repository.
2. Install dependencies:

   `pipenv install`

3. Navigate into the server folder:

   `cd server`

4. Run database migrations:

   `pipenv run python -m flask --app app db upgrade`

5. Seed the database:

   `pipenv run python seed.py`

6. Start the server:

   `pipenv run python app.py`

The API runs at `http://127.0.0.1:5555`.
