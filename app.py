from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

@app.route('/')
def home():
    return "YouTube Family Invitation Bot is Running!"

@app.route('/invite', methods=['POST'])
def invite():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        invite_emails = data.get('inviteEmails', '').split('\n')
        
        if not email or not password or not invite_emails:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Simulate sending invites (Replace this with actual automation logic)
        print(f"Logging in as {email} and sending invites to: {invite_emails}")
        
        return jsonify({'message': 'Invitations sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
