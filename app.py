from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import pandas as pd
from qa_script import transcribe_audio, evaluate_call, process_calls

app = Flask(__name__, static_folder='.')
CORS(app)

# Load users from JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": []}

# Save users to JSON file
def save_users(users_data):
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=2)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    users_data = load_users()
    user = next((u for u in users_data['users'] if u['username'].lower() == username.lower() and u['password'] == password), None)
    
    if user:
        return jsonify({"success": True, "username": username})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    users_data = load_users()
    
    # Check if username already exists
    if any(u['username'] == username for u in users_data['users']):
        return jsonify({"success": False, "message": "Username already exists"}), 400
    
    # Add new user
    users_data['users'].append({
        "username": username,
        "password": password,
        "data": {}
    })
    save_users(users_data)
    
    return jsonify({"success": True, "username": username})

@app.route('/api/review', methods=['POST'])
def review_calls():
    data = request.get_json()
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        if pd.isna(row['transcription']) or row['transcription'] == "":
            transcription = transcribe_audio(row['recording'])
            df.at[index, 'transcription'] = transcription
            review = evaluate_call(transcription, row['name'])
            df.at[index, 'review'] = review
    return jsonify(df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True) 