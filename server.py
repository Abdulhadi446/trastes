"""
Flask server for St. George's School Learning App
Run: python server.py
"""
from flask import Flask, send_from_directory, request, jsonify, make_response
import requests
import os

app = Flask(__name__)

# Manual CORS headers
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Serve main index.html

# Create templates route
TEMPLATES_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve main index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico')

# Serve static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Serve english folder
@app.route('/english/<path:filename>')
def english_file(filename):
    return send_from_directory('english', filename)

# Serve maths folder  
@app.route('/maths/<path:filename>')
def maths_file(filename):
    return send_from_directory('maths', filename)

# Serve science folder
@app.route('/science/<path:filename>')
def science_file(filename):
    return send_from_directory('science', filename)

# Serve urdu folder
@app.route('/urdu/<path:filename>')
def urdu_file(filename):
    return send_from_directory('urdu', filename)

# Serve tests folder
@app.route('/tests/<path:filename>')
def tests_file(filename):
    return send_from_directory('tests', filename)

# Chat API endpoint
API_URL = "https://sodeom.com/v1/chat/completions"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    try:
        resp = requests.post(API_URL, json={
            "model": data.get('model', 'gpt-4o-mini'),
            "messages": data.get('messages', []),
            "max_tokens": data.get('max_tokens', 200)
        }, timeout=30)
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Make quiz work without API
@app.route('/grade', methods=['POST'])
def grade():
    data = request.json
    answers = data.get('answers', {})
    correct = data.get('correct', {})
    score = 0
    for q, ans in answers.items():
        if ans.lower() == correct.get(q, '').lower():
            score += 1
    total = len(correct)
    grade = 'A+' if score >= total*0.9 else 'A' if score >= total*0.8 else 'B' if score >= total*0.7 else 'C' if score >= total*0.6 else 'F'
    return jsonify({"score": score, "total": total, "grade": grade})

if __name__ == '__main__':
    print("=" * 40)
    print("🚀 St. George's School Learning Server")
    print("=" * 40)
    print("🌐 Open: http://localhost:5000")
    print("📚 Available routes:")
    print("   /              - Main page")
    print("   /english/      - English topics")
    print("   /maths/       - Maths topics")
    print("   /science/     - Science topics")
    print("   /urdu/        - Urdu topics")
    print("   /tests/        - Test papers")
    print("   /chat         - AI chat")
    print("=" * 40)
    app.run(port=5000, debug=True)