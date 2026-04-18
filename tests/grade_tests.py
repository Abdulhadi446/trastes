#!/usr/bin/env python3
"""
Test Grader using Sodeom AI API
Free OpenAI-compatible AI API via GitHub Models
"""
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://sodeom.com/v1",
    api_key="any",  # Can use any string
)

def grade_english_test(answers: dict) -> dict:
    """Grade English test using AI"""
    prompt = f"""You are a teacher grading a Class IX English aptitude test.
Check each answer and give a score out of 8, with feedback.

Student Answers:
1. Comprehension: {answers.get('q1', 'N/A')}
2. Essay: {answers.get('q2', 'N/A')}
3. Letter: {answers.get('q3', 'N/A')}
4. Idioms: {answers.get('q4', 'N/A')}
5. Verbs: {answers.get('q5', 'N/A')}
6. Active/Passive: {answers.get('q6', 'N/A')}
7. Do as Directed: {answers.get('q7', 'N/A')}
8. Transformation: {answers.get('q8', 'N/A')}

Grade strictly. Return in this format:
Score: X/8
Feedback:
- Q1: [Correct/Incorrect] - [reason]
- Q2: [Correct/Incorrect] - [reason]
...
Grade: [A+/A/B/C/F]
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"result": response.choices[0].message.content}

def grade_maths_test(answers: dict) -> dict:
    """Grade Maths test using AI"""
    prompt = f"""You are a teacher grading a Class IX Maths aptitude test.
Check each answer and give a score out of 8, with feedback.

Student Answers:
1. Triangle angles sum: {answers.get('q1', 'N/A')}° (correct: 180)
2. Square root: {answers.get('q2', 'N/A')} (correct: 12)
3. Sets intersection: {answers.get('q3', 'N/A')} (correct: {{3}})
4. Simplify 5+3*2: {answers.get('q4', 'N/A')} (correct: 11)
5. Factorization: {answers.get('q5', 'N/A')} (correct: 2(x+2))
6. Triangle area: {answers.get('q6', 'N/A')} (correct: 12)
7. Brackets 2(x+3): {answers.get('q7', 'N/A')} (correct: 2x+6)
8. BODMAS (10+5)/3: {answers.get('q8', 'N/A')} (correct: 5)"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"result": response.choices[0].message.content}

def grade_test_by_subject(subject: str, answers: dict) -> dict:
    """Generic test grader"""
    if subject.lower() == "english":
        return grade_english_test(answers)
    elif subject.lower() == "maths":
        return grade_maths_test(answers)
    else:
        return {"error": "Subject not supported"}

def review_essay(essay: str) -> dict:
    """Get AI feedback on essay"""
    prompt = f"""You are a teacher. Provide feedback on this Class IX student's essay:
    
{essay}

Provide:
1. Grade (A+/A/B/C/F)
2. Strengths (2-3 points)
3. Areas to improve (2-3 points)
4. Suggestion for improvement"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"feedback": response.choices[0].message.content}

def check_urdu_essay(essay: str) -> dict:
    """Check Urdu essay"""
    prompt = f"""آپ ایک استاد ہیں۔ اس اردو مضمون کا جائزہ لیں:

{essay}

دیھیں:
1. درجہ (A+/A/B/C/F)
2. خوبیایں (2-3)
3. بہتری کی گنجائش (2-3)
4. تجویز"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"feedback": response.choices[0].message.content}

# Example usage
if __name__ == "__main__":
    # Example: Grade English test
    eng_answers = {
        "q1": "West",
        "q2": "beautiful",
        "q3": "Principal",
        "q4": "very easy",
        "q5": "went",
        "q6": "A letter is written by Ali",
        "q7": "The boys run.",
        "q8": "He is wiser than others."
    }
    
    print("Grading English test...")
    result = grade_english_test(eng_answers)
    print(result["result"])
    
    print("\n" + "="*50 + "\n")
    
    # Example: Get essay feedback
    sample_essay = "My school is a beautiful place. It has large buildings and green gardens. I love my teachers. They are very kind and helpful."
    
    print("Getting essay feedback...")
    feedback = review_essay(sample_essay)
    print(feedback["feedback"])