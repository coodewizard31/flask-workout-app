from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

# 1. ------Workout Model ----
class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # TABLE CONSTRAINT 1: Duration must be greater than 0
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    # -----The relationship to join table------
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan')

    # MODEL VALIDATION 1
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes!")
        return duration


# 2. -----Exercise Model -----
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    # TABLE CONSTRAINT 2: Name cannot be empty
    __table_args__ = (
        CheckConstraint("length(name) > 0", name='check_exercise_name_not_empty'),
    )

    # Relationship to join table
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan')

    # -----Model Validation 2
    @validates('category')
    def validate_category(self, key, category_name):
        allowed = ['Cardio', 'Strength', 'Flexibility', 'HIIT']
        if category_name not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return category_name



# 3.------Workout exercise (JOIN TABLE)
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    # TABLE CONSTRAINT 3
    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps >= 0', name='check_reps_positive'),
    )