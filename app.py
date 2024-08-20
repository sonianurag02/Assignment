from flask import Flask, request, jsonify
import sqlite3
import openai
import os

app = Flask(__name__)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize SQLite database
def init_db():
    with sqlite3.connect('chatbot.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            service TEXT
        )''')
        conn.commit()

init_db()

@app.route('/welcome', methods=['GET'])
def welcome_message():
    return jsonify({"message": "Hi there! I'm here to help you connect with top-rated contractors. How can I assist you today?"})

@app.route('/submit_lead', methods=['POST'])
def submit_lead():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    service = data.get('service')
    
    with sqlite3.connect('chatbot.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leads (name, email, phone, service) VALUES (?, ?, ?, ?)', 
                       (name, email, phone, service))
        conn.commit()
    
    return jsonify({"message": "Lead information captured successfully!"})

@app.route('/faq', methods=['GET'])
def get_faq():
    query = request.args.get('query')
    
    # Use fine-tuned model
    try:
        response = openai.Completion.create(
            model='YOUR_FINE_TUNED_MODEL_ID',  # Replace with your fine-tuned model ID
            prompt=f"Answer this question: {query}",
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        answer = f"An error occurred: {str(e)}"
    
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
