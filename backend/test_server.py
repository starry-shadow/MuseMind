from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/journal', methods=['POST'])
def create_journal_entry():
    data = request.get_json()
    entry_text = data.get('entry', '')
    
    if not entry_text:
        return jsonify({'error': 'No journal entry provided'}), 400
        
    try:
        # Create a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save the entry
        with open(f"../MuseMind/wwwroot/journal_entries/{timestamp}_entry.txt", "w") as f:
            f.write(entry_text)
        
        # Save a test response
        with open(f"../MuseMind/wwwroot/journal_entries/{timestamp}_response.txt", "w") as f:
            f.write("This is a test response. Your entry was received successfully.")
            
        return jsonify({
            'success': True,
            'timestamp': timestamp
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/journal/<timestamp>', methods=['GET'])
def get_journal_response(timestamp):
    try:
        # Read the response file
        response_path = f"../MuseMind/wwwroot/journal_entries/{timestamp}_response.txt"
        
        if not os.path.exists(response_path):
            return jsonify({'error': 'Response not found'}), 404
            
        with open(response_path, 'r') as f:
            response_text = f.read()
            
        return jsonify({
            'response': response_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)