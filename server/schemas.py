
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSummarySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    exercise = fields.Nested(ExerciseSummarySchema, dump_only=True)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    equipment_needed = fields.Bool(required=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )


class WorkoutExerciseCreateSchema(Schema):
    reps = fields.Int(allow_none=True, load_default=None)
    sets = fields.Int(allow_none=True, load_default=None)
    duration_seconds = fields.Int(allow_none=True, load_default=None)

    @validates_schema
    def validate_values(self, data, **kwargs):
        for field in ("reps", "sets", "duration_seconds"):
            value = data.get(field)

            if value is not None and value <= 0:
                raise ValidationError(
                    f"{field} must be greater than zero.",
                    field_name=field
                )

        if all(data.get(field) is None for field in (
            "reps", "sets", "duration_seconds"
        )):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds."
            )


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_create_schema = WorkoutExerciseCreateSchema()
