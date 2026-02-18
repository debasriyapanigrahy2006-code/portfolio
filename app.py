from flask import Flask, render_template, json, request, jsonify
import os
from groq import Groq

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load resume data
try:
    with open('cleaned_resume.txt', 'r', encoding='utf-8') as f:
        RESUME_TEXT = f.read()
except FileNotFoundError:
    try:
        with open('raw_text.txt', 'r', encoding='utf-8') as f:
            RESUME_TEXT = f.read()
    except FileNotFoundError:
        RESUME_TEXT = "Resume data not found."

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    # Fallback for local testing if .env is missing or not loaded, though not recommended for production
    # But better to just warn or fail. 
    # For this specific user request, let's try to be helpful and print a warning.
    print("WARNING: GROQ_API_KEY not found in environment variables.")
    
client = Groq(api_key=api_key)

def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant for Debasriya Panigrahy's portfolio. Answer questions based ONLY on the following resume content. If the answer is not in the resume, say you don't know.\n\nRESUME CONTENT:\n{RESUME_TEXT}"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        bot_response = completion.choices[0].message.content
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
