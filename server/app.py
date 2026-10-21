import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from datetime import datetime

from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
# Get absolute path to the directory containing app.py
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Explicitly set database path inside the server folder
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Schema instances
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

# -----Workout endpoints-----

@app.route('/workouts', methods=['GET'])
def get_workouts():
    all_workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(all_workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json() or {}
    try:
        data = workout_schema.load(json_data)
        
        # Convert date string to python date object if needed
        date_val = data['date']
        if isinstance(date_val, str):
            date_val = datetime.strptime(date_val, '%Y-%m-%d').date()

        new_workout = Workout(
            date=date_val,
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify(workout_schema.dump(new_workout)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} deleted successfully"}), 200


# ----Exercise endpoints-------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    all_exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(all_exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json() or {}
    try:
        data = exercise_schema.load(json_data)
        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        db.session.add(new_exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(new_exercise)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} deleted successfully"}), 200


# Adding exercise to workouts

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    json_data = request.get_json() or {}
    try:
        data = workout_exercise_schema.load(json_data)
        
        new_entry = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify(workout_exercise_schema.dump(new_entry)), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)