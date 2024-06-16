import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# URL of your Rasa server
RASA_SERVER_URL = 'http://localhost:5005/webhooks/rest/webhook'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # Forward the message to Rasa server
    rasa_response = requests.post(RASA_SERVER_URL, json={'message': message})
    
    if rasa_response.status_code == 200:
        # Extract the text from Rasa response
        rasa_data = rasa_response.json()
        if rasa_data and isinstance(rasa_data, list) and 'text' in rasa_data[0]:
            response_text = rasa_data[0]['text']
            return jsonify({'response': response_text})
        else:
            return jsonify({'error': 'Invalid response from Rasa'}), 500
    else:
        return jsonify({'error': 'Failed to connect to Rasa server'}), 500

if __name__ == '__main__':
    app.run(debug=True)
