from flask import request, jsonify, abort
from flask_login import login_required, current_user
from app import app, db
from models import Meal
from datetime import datetime

@app.route('/meals', methods=['POST'])
@login_required
def add_meal():
    data = request.get_json()
    if not data or 'name' not in data or 'date_time' not in data or 'is_diet_compliant' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    meal = Meal(
        name=data['name'],
        description=data.get('description', ''),
        date_time=datetime.fromisoformat(data['date_time']),
        is_diet_compliant=data['is_diet_compliant'],
        user_id=current_user.id
    )
    db.session.add(meal)
    db.session.commit()
    return jsonify(meal.id), 201

@app.route('/meals/<int:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        abort(404)
    return jsonify({
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'date_time': meal.date_time.isoformat(),
        'is_diet_compliant': meal.is_diet_compliant
    })

@app.route('/meals/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
    if not meal:
        abort(404)
    data = request.get_json()
    meal.name = data.get('name', meal.name)
    meal.description = data.get('description', meal.description)
    meal.date_time = datetime.fromisoformat(data['date_time']) if 'date_time' in data else meal.date_time
    meal.is_diet_compliant = data.get('is_diet_compliant', meal.is_diet_compliant)
    db.session.commit()
    return jsonify({'success': 'Meal updated'})

@app.route('/meals/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.filter_by(id=meal_text_id, user_id=current_user.id).first()
    if not meal:
        abort(404)
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'success': 'Meal deleted'})

@app.route('/meals', methods=['GET'])
@login_required
def list_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'date_time': meal.date_time.isoformat(),
            'is_diet_compliant': meal.is_diet_compliant
        } for meal in meals
    ])
