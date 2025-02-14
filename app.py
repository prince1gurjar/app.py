from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time

app = Flask(__name__)
CORS(app)

@app.route('/send-invites', methods=['POST'])
def send_invites():
    try:
        data = request.json
        gmail_accounts = data.get("gmail_accounts", [])
        invite_emails = data.get("invite_emails", [])

        if not gmail_accounts or not invite_emails:
            return jsonify({"error": "Missing Gmail accounts or invite emails"}), 400

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")  # Run without GUI
        
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        
        results = []

        for gmail, password in gmail_accounts:
            driver.get("https://accounts.google.com/signin")
            time.sleep(2)
            
            # Enter Gmail
            email_input = driver.find_element(By.ID, "identifierId")
            email_input.send_keys(gmail)
            email_input.send_keys(Keys.ENTER)
            time.sleep(2)
            
            # Enter Password
            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            time.sleep(5)
            
            # Navigate to YouTube Family Sharing Page
            driver.get("https://www.youtube.com/family")
            time.sleep(3)
            
            # Click on Manage Invitation
            manage_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Manage')]" )
            manage_button.click()
            time.sleep(3)
            
            # Send Invites
            for invite_email in invite_emails:
                invite_input = driver.find_element(By.XPATH, "//input[@type='email']")
                invite_input.send_keys(invite_email)
                invite_input.send_keys(Keys.ENTER)
                time.sleep(2)
                
            # Confirm Invitation
            send_invite_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]" )
            send_invite_button.click()
            time.sleep(5)
            
            results.append(f"Invites sent successfully from {gmail}")
        
        driver.quit()
        
        return jsonify({"result": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
