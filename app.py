from flask import Flask, request, jsonify, render_template
import mysql.connector
import bcrypt
import subprocess

app = Flask(__name__)

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",  # Replace with your MySQL root password
    database="asl_detection"
)

# Global variable to store the inference process
inference_process = None

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode to store as a string

# Verify a password
def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result and verify_password(password, result[0]):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

# Register Endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed_password = hash_password(password)

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        return jsonify({'success': True, 'message': 'User registered successfully!'})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': str(err)})

# Start Inference Endpoint
@app.route('/start_inference', methods=['POST'])
def start_inference():
    global inference_process
    if inference_process is None:
        inference_process = subprocess.Popen(['python', 'asl_scripts/inference_classifier.py'])
        return jsonify({'success': True, 'message': 'ASL detection started!'})
    else:
        return jsonify({'success': False, 'message': 'ASL detection is already running!'})

# Stop Inference Endpoint
@app.route('/stop_inference', methods=['POST'])
def stop_inference():
    global inference_process
    if inference_process:
        inference_process.terminate()
        inference_process = None
        return jsonify({'success': True, 'message': 'ASL detection stopped!'})
    else:
        return jsonify({'success': False, 'message': 'ASL detection is not running!'})

if __name__ == '__main__':
    app.run(debug=True)
