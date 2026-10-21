from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    # SCHEMA VALIDATION 1: Allowed options check
    category = fields.Str(required=True, validate=validate.OneOf(
        ['Cardio', 'Strength', 'Flexibility', 'HIIT'], 
        error="Invalid category chosen"
    ))
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    # SCHEMA VALIDATION 2: Non-negative check
    reps = fields.Int(validate=validate.Range(min=0, error="Reps cannot be negative"))
    sets = fields.Int(validate=validate.Range(min=0, error="Sets cannot be negative"))
    duration_seconds = fields.Int(validate=validate.Range(min=0, error="Duration cannot be negative"))
    
    # Include exercise detail inside workout response (Stretch goal)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    # SCHEMA VALIDATION 3: Range check
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Must be at least 1 minute"))
    notes = fields.Str(allow_none=True)
    
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)