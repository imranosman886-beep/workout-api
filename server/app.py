
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_create_schema
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return jsonify({"message": "Workout API is running"})


# WORKOUT ROUTES

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})

        workout = Workout(**data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": "Workout deleted successfully"}), 200


# EXERCISE ROUTES

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})

        exercise = Exercise(**data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": "Exercise deleted successfully"}), 200


# ADD EXERCISE TO WORKOUT

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    existing = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id
    ).first()

    if existing:
        return jsonify({"error": "Exercise already belongs to this workout"}), 409

    try:
        data = workout_exercise_create_schema.load(
            request.get_json() or {}
        )

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **data
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise added to workout",
            "workout_exercise": {
                "id": workout_exercise.id,
                "workout_id": workout_exercise.workout_id,
                "exercise_id": workout_exercise.exercise_id,
                "reps": workout_exercise.reps,
                "sets": workout_exercise.sets,
                "duration_seconds": workout_exercise.duration_seconds
            }
        }), 201

    except ValidationError as error:
        db.session.rollback()
        return jsonify({"errors": error.messages}), 400

    except (ValueError, TypeError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
