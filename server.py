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

@app.route('/chat', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/grade', methods=['GET', 'POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
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

# Generate dynamic test
@app.route('/generate-test', methods=['GET', 'POST', 'OPTIONS'])
def generate_test():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    data = request.json or {}
    subject = data.get('subject', 'English')
    
    prompt = f"""Generate a Class IX {subject} test with EXACTLY 10 questions in this JSON format:

{{
  "questions": [
    {{
      "type": "mcq",
      "question": "Question text here?",
      "options": ["a) Option A", "b) Option B", "c) Option C", "d) Option D"],
      "correct": "a"
    }},
    {{
      "type": "fill",
      "question": "The capital of France is ___.",
      "correct": "Paris"
    }},
    {{
      "type": "short",
      "question": "What is photosynthesis?",
      "correct": "The process by which plants convert sunlight into food using chlorophyll."
    }},
    {{
      "type": "long",
      "question": "Write an essay on 'The Importance of Education' (100-150 words)",
      "correct": "Essay should cover: education empowers individuals, develops critical thinking, creates opportunities, builds society."
    }}
  ]
}}

Rules:
- Include 3 MCQs, 3 Fill-in-blanks, 2 Short answer, 2 Long answer
- Make questions appropriate for Class IX (14-15 year olds)
- For mcq: correct answer should be just the letter (a, b, c, or d)
- For fill/short/long: provide a model answer
- Return ONLY valid JSON, no explanation
"""
    
    try:
        resp = requests.post(API_URL, json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000
        }, timeout=60)
        content = resp.json()['choices'][0]['message']['content']
        import json
        import re
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            test_data = json.loads(match.group())
            return jsonify(test_data)
        return jsonify({"error": "Failed to parse JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Grade dynamic test
@app.route('/grade-test', methods=['GET', 'POST', 'OPTIONS'])
def grade_test():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    data = request.json or {}
    questions = data.get('questions', [])
    answers = data.get('answers', {})
    
    prompt = f"""Grade this Class IX test. Compare student answers to model answers and provide score.

Questions and answers:
{json.dumps({'questions': questions, 'answers': answers}, indent=2)}

Return this JSON format:
{{
  "score": total_marks_obtained,
  "total": total_possible_marks,
  "grade": "letter grade",
  "feedback": "Overall feedback",
  "details": [
    {{"q": 1, "marks": 1, "feedback": "Brief feedback"}}
  ]
}}

Grading rules:
- MCQ: 1 mark each
- Fill in blank: 1 mark each  
- Short answer: 2 marks each
- Long answer: 5 marks each
- Grade: A+ (90%+), A (80%+), B (70%+), C (60%+), F (<60%)
- Be fair and generous with partial marks
- Return ONLY valid JSON
"""
    
    try:
        resp = requests.post(API_URL, json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }, timeout=60)
        content = resp.json()['choices'][0]['message']['content']
        import json
        import re
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            result = json.loads(match.group())
            return jsonify(result)
        return jsonify({"error": "Failed to parse JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Make quiz work without API
@app.route('/grade', methods=['GET', 'POST', 'OPTIONS'])
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
    print("   Or: http://0.0.0.0:5000")
    print("📚 Available routes:")
    print("   /              - Main page")
    print("   /english/      - English topics")
    print("   /maths/       - Maths topics")
    print("   /science/     - Science topics")
    print("   /urdu/        - Urdu topics")
    print("   /tests/        - Test papers")
    print("   /chat         - AI chat")
    print("=" * 40)
    app.run(host='0.0.0.0', port=5000, debug=True)