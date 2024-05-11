from flask import request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, bcrypt
from models import User

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Hash password and create new user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({'success': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': 'Logged out successfully'}), 200
