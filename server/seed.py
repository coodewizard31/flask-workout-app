#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Clearing database tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding Exercises...")
    ex1 = Exercise(name="Push Ups", category="Strength", equipment_needed=False)
    ex2 = Exercise(name="Karura Forest Jog", category="Cardio", equipment_needed=False)
    ex3 = Exercise(name="Plank Hold", category="Flexibility", equipment_needed=False)
    ex4 = Exercise(name="Dumbbell Squats", category="Strength", equipment_needed=True)

    db.session.add_all([ex1, ex2, ex3, ex4])
    db.session.commit()

    print("Seeding Workouts...")
    w1 = Workout(date=date(2026, 10, 15), duration_minutes=45, notes="Morning workout before work")
    w2 = Workout(date=date(2026, 10, 20), duration_minutes=30, notes="Evening cardio at Uhuru Park")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Adding Exercises to Workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, reps=20, sets=3)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex4.id, reps=12, sets=4)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex2.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeded successfully!")