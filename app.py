from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datetime import datetime

app = Flask(__name__)

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# To store chat history
chat_history = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    data = request.get_json()
    user_input = data.get('message', '').lower()

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Custom responses for specific queries
    if 'date' in user_input or 'day' in user_input:
        response = f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."
        return jsonify({'response': response})

    # Tokenize user input and append to chat history
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    if chat_history is None:
        chat_history = new_user_input_ids
    else:
        chat_history = torch.cat([chat_history, new_user_input_ids], dim=-1)

    # Generate a response
    chat_history_ids = model.generate(chat_history, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, chat_history.shape[-1]:][0], skip_special_tokens=True)

    # Update chat history
    chat_history = chat_history_ids

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
