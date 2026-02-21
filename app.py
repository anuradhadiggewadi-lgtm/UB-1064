from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
import json
import socket
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
CORS(app)

# Database setup
DATABASE = 'zenstress.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            age INTEGER,
            heart_rate REAL,
            sleep_hours REAL,
            steps_count INTEGER,
            sleep_quality REAL,
            day_rating INTEGER,
            stress_level TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

# Initialize ML model
model = None
scaler = StandardScaler()

def initialize_model():
    """Initialize and train the stress prediction model"""
    global model, scaler
    
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    
    # Features: heart_rate, sleep_hours, steps_count, sleep_quality
    X_train = np.random.rand(n_samples, 4)
    X_train[:, 0] = X_train[:, 0] * 60 + 60  # Heart rate: 60-120 bpm
    X_train[:, 1] = X_train[:, 1] * 8 + 4     # Sleep: 4-12 hours
    X_train[:, 2] = X_train[:, 2] * 15000     # Steps: 0-15000
    X_train[:, 3] = X_train[:, 3] * 10        # Sleep quality: 0-10
    
    # Generate target stress levels (0=Low, 1=Medium, 2=High)
    # Stress increases with:
    # - High heart rate
    # - Low sleep hours
    # - Very high or very low steps
    # - Low sleep quality
    stress_score = (
        (X_train[:, 0] - 70) / 20 +           # Higher HR -> more stress
        (X_train[:, 1] - 8) / -4 +            # Lower sleep -> more stress
        (X_train[:, 3] - 5) / -5              # Lower sleep quality -> more stress
    )
    
    y_train = np.zeros(n_samples)
    y_train[stress_score < -0.5] = 0  # Low stress
    y_train[stress_score >= -0.5] = 1  # Medium stress
    y_train[stress_score > 0.5] = 2   # High stress
    y_train = y_train.astype(int)
    
    # Train model
    X_scaled = scaler.fit_transform(X_train)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y_train)
    
    print("Model initialized and trained successfully")

def predict_stress(heart_rate, sleep_hours, steps_count, sleep_quality, age=30, day_rating=3):
    """Predict stress level from wearable data"""
    if model is None:
        initialize_model()
    
    # Prepare input features (original 4 features for compatibility with existing model)
    features = np.array([[heart_rate, sleep_hours, steps_count, sleep_quality]])
    features_scaled = scaler.transform(features)
    
    # Predict
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    
    # Adjust prediction based on age and day rating
    # Older people may have different stress patterns
    age_factor = 0
    if age < 25:
        age_factor = 0.1  # Younger people might have slightly higher stress
    elif age > 50:
        age_factor = -0.05  # Older people might manage stress better
    
    # Day rating affects stress (1=Very Bad, 5=Excellent)
    day_factor = (3 - day_rating) * 0.15  # Bad day increases stress probability
    
    # Adjust probabilities
    adjustment = age_factor + day_factor
    probabilities = probabilities.copy()
    
    # Shift probabilities based on adjustment
    if adjustment > 0:  # Increase stress
        if prediction < 2:  # Not already high
            probabilities[prediction] -= min(adjustment, probabilities[prediction] * 0.3)
            probabilities[min(2, prediction + 1)] += min(adjustment, 0.3)
    elif adjustment < 0:  # Decrease stress
        if prediction > 0:  # Not already low
            probabilities[prediction] -= min(abs(adjustment), probabilities[prediction] * 0.3)
            probabilities[max(0, prediction - 1)] += min(abs(adjustment), 0.3)
    
    # Normalize probabilities
    probabilities = probabilities / probabilities.sum()
    
    # Get new prediction
    prediction = np.argmax(probabilities)
    
    stress_levels = ['Low', 'Medium', 'High']
    predicted_level = stress_levels[prediction]
    confidence = probabilities[prediction] * 100
    
    return predicted_level, confidence, probabilities

def analyze_stress_factors(heart_rate, sleep_hours, steps_count, sleep_quality, age, day_rating, stress_level):
    """Analyze which factors contributed to the stress level"""
    insights = []
    
    # Analyze sleep hours
    if sleep_hours < 6:
        insights.append(f"⚠️ Low sleep duration ({sleep_hours} hours) - You're getting insufficient sleep which significantly increases stress")
    elif sleep_hours > 9:
        insights.append(f"⚠️ Excessive sleep ({sleep_hours} hours) - Oversleeping can indicate stress or fatigue")
    elif sleep_hours >= 7 and sleep_hours <= 9 and stress_level != 'Low':
        insights.append(f"✓ Good sleep duration ({sleep_hours} hours)")
    
    # Analyze sleep quality
    if sleep_quality < 5:
        insights.append(f"⚠️ Poor sleep quality ({sleep_quality}/10) - Low quality sleep prevents proper recovery")
    elif sleep_quality >= 7:
        insights.append(f"✓ Good sleep quality ({sleep_quality}/10)")
    
    # Analyze heart rate
    if heart_rate > 90:
        insights.append(f"⚠️ Elevated heart rate ({heart_rate} bpm) - Higher than normal resting heart rate indicates stress")
    elif heart_rate > 80:
        insights.append(f"⚠️ Slightly elevated heart rate ({heart_rate} bpm)")
    elif heart_rate >= 60 and heart_rate <= 75:
        insights.append(f"✓ Healthy resting heart rate ({heart_rate} bpm)")
    
    # Analyze step count
    if steps_count < 5000:
        insights.append(f"⚠️ Low physical activity ({steps_count:,} steps) - Insufficient movement can increase stress levels")
    elif steps_count >= 8000:
        insights.append(f"✓ Good physical activity ({steps_count:,} steps)")
    
    # Analyze day rating
    if day_rating <= 2:
        insights.append(f"⚠️ Difficult day reported - Your mood significantly impacts stress perception")
    elif day_rating >= 4:
        insights.append(f"✓ Positive day reported - Good mood helps reduce stress")
    
    # Analyze age factor
    if age < 25 and stress_level == 'High':
        insights.append(f"ℹ️ Younger age ({age}) - Young adults often experience higher stress due to life transitions")
    
    # Summary insight
    warning_count = sum(1 for insight in insights if insight.startswith('⚠️'))
    if warning_count == 0:
        insights.insert(0, "✅ Overall good health metrics - Low stress predicted")
    elif warning_count >= 3:
        insights.insert(0, f"⚠️ Multiple stress factors detected ({warning_count} areas of concern)")
    else:
        insights.insert(0, f"⚠️ Some stress factors detected ({warning_count} area{'s' if warning_count > 1 else ''} of concern)")
    
    return insights

def get_recommendations(stress_level):
    """Get recommendations based on stress level"""
    recommendations = {
        'Low': [
            'Continue maintaining your healthy lifestyle!',
            'Keep up your regular exercise routine',
            'Maintain consistent sleep schedule',
            'Practice mindfulness or meditation daily'
        ],
        'Medium': [
            'Try to get at least 7-8 hours of sleep tonight',
            'Take short breaks every hour during work',
            'Go for a 20-minute walk to reduce stress',
            'Practice deep breathing exercises',
            'Listen to calming music for 15 minutes',
            'Consider reducing caffeine intake'
        ],
        'High': [
            'Prioritize rest - aim for 8+ hours of sleep',
            'Take a 30-minute walk in nature',
            'Practice 10 minutes of meditation',
            'Try progressive muscle relaxation',
            'Hydrate well with water',
            'Avoid screens 1 hour before bed',
            'Consider talking to a friend or counselor',
            'Do light stretching exercises',
            'Take a warm bath or shower',
            'Eat a nutritious meal'
        ]
    }
    return recommendations.get(stress_level, [])

def get_stress_media(stress_level):
    """Get music recommendations based on stress level"""
    media = {
        'Low': {
            'songs': [
                {'title': 'Peaceful Morning', 'url': 'https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0', 'type': 'ambient', 'language': 'english'},
                {'title': 'Nature Sounds', 'url': 'https://www.youtube.com/embed/q76bMs-NwRk?autoplay=0', 'type': 'nature', 'language': 'english'},
                {'title': 'healing inner angry', 'url': 'https://www.youtube.com/embed/6m2Ma8uX74s?autoplay=0', 'type': 'peaceful', 'language': 'english'},
               
            ]
        },
        'Medium': {
            'songs': [
                {'title': 'Calm Music', 'url': 'https://www.youtube.com/embed/f-i_nJLG2Is?autoplay=0', 'type': 'calm', 'language': 'english'},
                {'title': 'Deep Sleep Music', 'url': 'https://www.youtube.com/embed/b4AkjHqDDK8?autoplay=0', 'type': 'sleep', 'language': 'english'},
                {'title': 'Relaxing Music', 'url': 'https://www.youtube.com/embed/QjDnjoaUJtI?autoplay=0', 'type': 'relaxing', 'language': 'english'},
            ]
        },
        'High': {
            'songs': [
                {'title': 'Relaxing music for stress relief', 'url': 'https://www.youtube.com/embed/YolaW-27tOo?autoplay=0', 'type': 'emergency', 'language': 'english'},
                {'title': 'calming music', 'url': 'https://www.youtube.com/embed/cDQ-krl38yE?autoplay=0', 'type': 'instant', 'language': 'english'},
                {'title': 'Anxiety Relief Music', 'url': 'https://www.youtube.com/embed/iWb6K61NMKo?autoplay=0', 'type': 'anxiety', 'language': 'english'},
                {'title': '528 Hz Music Therapy', 'url': 'https://www.youtube.com/embed/Zr8uhuqH-YE?autoplay=0', 'type': 'therapy', 'language': 'english'},
               
            ]
        }
    }
    return media.get(stress_level, {'songs': []})

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if request.method == 'POST':
        data = request.get_json() or request.form
        email = data.get('email')
        password = data.get('password')
        
        # Accept any email and password as long as they're provided
        if email and password:
            conn = get_db()
            cursor = conn.cursor()
            
            # Check if user exists
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if user:
                # User exists - verify password
                if user['password'] == password:
                    session['email'] = email
                    session['name'] = user['name']
                    session['user_id'] = user['id']
                    conn.close()
                    return jsonify({'success': True, 'redirect': '/dashboard'})
                else:
                    conn.close()
                    return jsonify({'success': False, 'error': 'Invalid password'})
            else:
                # New user - create account
                name = email.split('@')[0].title() if '@' in email else 'User'
                cursor.execute('INSERT INTO users (email, password, name) VALUES (?, ?, ?)',
                             (email, password, name))
                conn.commit()
                user_id = cursor.lastrowid
                
                session['email'] = email
                session['name'] = name
                session['user_id'] = user_id
                conn.close()
                return jsonify({'success': True, 'redirect': '/dashboard'})
        else:
            return jsonify({'success': False, 'error': 'Please provide both email and password'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout handler"""
    session.clear()
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=session.get('name'))

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for stress prediction"""
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        
        # Get wearable data
        age = float(data.get('age', 30))
        heart_rate = float(data.get('heartRate', 70))
        sleep_hours = float(data.get('sleepHours', 7))
        steps_count = float(data.get('stepsCount', 8000))
        sleep_quality = float(data.get('sleepQuality', 7))
        day_rating = float(data.get('dayRating', 3))
        
        # Predict stress
        stress_level, confidence, probabilities = predict_stress(
            heart_rate, sleep_hours, steps_count, sleep_quality, age, day_rating
        )
        
        # Analyze stress factors
        insights = analyze_stress_factors(
            heart_rate, sleep_hours, steps_count, sleep_quality, age, day_rating, stress_level
        )
        
        # Get recommendations and media
        recommendations = get_recommendations(stress_level)
        media = get_stress_media(stress_level)
        
        # Save prediction to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions 
            (user_id, age, heart_rate, sleep_hours, steps_count, sleep_quality, day_rating, stress_level, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], age, heart_rate, sleep_hours, steps_count, sleep_quality, day_rating, stress_level, round(confidence, 2)))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'stressLevel': stress_level,
            'confidence': round(confidence, 2),
            'probabilities': {
                'Low': round(probabilities[0] * 100, 2),
                'Medium': round(probabilities[1] * 100, 2),
                'High': round(probabilities[2] * 100, 2)
            },
            'insights': insights,
            'recommendations': recommendations,
            'media': media,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict_history', methods=['GET'])
def predict_history():
    """Get user's prediction history"""
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get last 10 predictions
        cursor.execute('''
            SELECT id, age, heart_rate, sleep_hours, steps_count, sleep_quality, 
                   day_rating, stress_level, confidence, timestamp
            FROM predictions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 10
        ''', (session['user_id'],))
        
        predictions = []
        for row in cursor.fetchall():
            predictions.append({
                'id': row['id'],
                'age': row['age'],
                'heartRate': row['heart_rate'],
                'sleepHours': row['sleep_hours'],
                'stepsCount': row['steps_count'],
                'sleepQuality': row['sleep_quality'],
                'dayRating': row['day_rating'],
                'stressLevel': row['stress_level'],
                'confidence': row['confidence'],
                'timestamp': row['timestamp']
            })
        
        conn.close()
        return jsonify({'success': True, 'history': predictions})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/clear_history', methods=['DELETE'])
def clear_history():
    """Clear user's prediction history"""
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Delete all predictions for the user
        cursor.execute('DELETE FROM predictions WHERE user_id = ?', (session['user_id'],))
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'Deleted {deleted_count} prediction(s)',
            'deleted_count': deleted_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/simulate_data', methods=['POST'])
def simulate_data():
    """Simulate wearable data for testing"""
    if 'email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Generate realistic wearable data
    data = {
        'age': np.random.randint(18, 65),
        'heartRate': np.random.randint(60, 100),
        'sleepHours': round(np.random.uniform(5, 9), 1),
        'stepsCount': np.random.randint(3000, 12000),
        'dayRating': np.random.randint(1, 6)
    }
    
    return jsonify(data)

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

if __name__ == '__main__':
    init_db()
    initialize_model()
    local_ip = get_local_ip()
    print("\n" + "="*70)
    print("✅ ZenStress Server Starting!")
    print("="*70)
    print(f"📱 Access on this device: http://localhost:5000")
    print(f"💻 Access on same network: http://{local_ip}:5000")
    print("="*70)
    print("\n🔗 Share these URLs with devices on the same Wi-Fi network")
    print("⚠️  Make sure Windows Firewall allows Python on port 5000")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

