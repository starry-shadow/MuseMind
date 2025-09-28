from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
from journal import process_journal_entry

load_dotenv()  # Load environment variables

app = Flask(__name__)
CORS(app)

# Configure Google's Generative AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/api/journal', methods=['POST'])
def create_journal_entry():
    data = request.get_json()
    entry_text = data.get('entry', '')

    if not entry_text:
        return jsonify({'error': 'No journal entry provided'}), 400
        
    try:
        import traceback
        print(f"\n=== Processing new journal entry ===")
        print(f"Received journal entry: {entry_text[:100]}...")  # Print first 100 chars of entry
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        # Process the journal entry using Gemini
        prompt = f"""You are Clio, the Muse of history. You help people process their personal stories.
        Read this journal entry and respond with empathy and wisdom, helping the person gain insight 
        into their experience. Keep the response encouraging and supportive. As a history buff, throw in some relelvant anecdotes.
        
        Journal entry: {entry_text}"""
        
        print("Generating response with Gemini...")
        try:
            response = model.generate_content(prompt)
            print(f"Gemini response received: {response.text[:100]}...")  # Print first 100 chars of response
        except Exception as gemini_error:
            print(f"Gemini API error: {str(gemini_error)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Gemini API error: {str(gemini_error)}")
        
        print("Processing journal entry...")
        # Save both the entry and the response
        try:
            timestamp = process_journal_entry(entry_text, response.text)
            print(f"Entry processed with timestamp: {timestamp}")
        except Exception as file_error:
            print(f"File operation error: {str(file_error)}")
            print(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"File operation error: {str(file_error)}")
        
        return jsonify({
            'success': True,
            'timestamp': timestamp
        })
    except Exception as e:
        error_msg = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print("\n=== Error in journal entry processing ===")
        print(error_msg)
        print("========================================\n")
        return jsonify({'error': str(e)}), 500

@app.route('/api/journal/<timestamp>', methods=['GET'])
def get_journal_response(timestamp):
    try:
        # Get the absolute path to the response file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        response_path = os.path.join(project_root, "MuseMind", "wwwroot", "journal_entries", f"{timestamp}_response.txt")
        
        if not os.path.exists(response_path):
            return jsonify({'error': 'Response not found'}), 404
            
        with open(response_path, 'r', encoding='utf-8') as f:
            response_text = f.read()
            
        return jsonify({
            'response': response_text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Create journal_entries directory if it doesn't exist
    os.makedirs('../MuseMind/wwwroot/journal_entries', exist_ok=True)
    app.run(host='localhost', port=5001, debug=True)