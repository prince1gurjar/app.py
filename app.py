from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Function to invite emails using Selenium
def invite_emails(host_email, host_password, invite_list):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Firefox(options=options)
    driver.get("https://accounts.google.com/signin")
    
    try:
        # Login process
        logging.info("Logging into Gmail account")
        email_input = driver.find_element(By.NAME, "identifier")
        email_input.send_keys(host_email)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(host_password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Go to YouTube family page
        driver.get("https://www.youtube.com/family/manage")
        time.sleep(5)
        
        for email in invite_list:
            logging.info(f"Sending invite to {email}")
            invite_box = driver.find_element(By.XPATH, "//input[@type='email']")
            invite_box.send_keys(email)
            invite_box.send_keys(Keys.RETURN)
            time.sleep(3)

        driver.quit()
        return {"status": "success", "message": "Invites sent successfully"}
    
    except Exception as e:
        driver.quit()
        logging.error(f"Error occurred: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.route('/send-invites', methods=['POST'])
def send_invites():
    try:
        data = request.json
        host_email = data.get("host_email")
        host_password = data.get("host_password")
        invite_list = data.get("invite_list", [])
        
        if not host_email or not host_password or not invite_list:
            return jsonify({"error": "Missing required fields"}), 400
        
        response = invite_emails(host_email, host_password, invite_list)
        return jsonify(response)
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
