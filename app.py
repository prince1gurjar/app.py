from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "YouTube Family Invitation Bot is Running!"

@app.route('/invite', methods=['POST'])
def invite():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        invite_emails = data.get("inviteEmails").split("\n")

        # Simulating invitation process
        time.sleep(2)
        
        return jsonify({"message": "Invitations sent successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
