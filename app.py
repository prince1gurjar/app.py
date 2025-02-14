from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "YouTube Family Invite Automation Backend is Running!"

@app.route('/invite', methods=['POST'])
def invite():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")
        invite_emails = data.get("inviteEmails").split("\n")

        # ✅ Define Chrome & ChromeDriver Paths
        CHROME_PATH = "/usr/bin/google-chrome"
        CHROMEDRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"

        options = webdriver.ChromeOptions()
        options.binary_location = CHROME_PATH  # Set Chrome binary path
        options.add_argument("--headless")  
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  
        options.add_argument("--disable-gpu")  
        options.add_argument("--disable-software-rasterizer")  
        options.add_argument("--disable-extensions")  
        options.add_argument("--window-size=1920x1080")

        # ✅ Use ChromeDriver with Explicit Path
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        # ✅ Login to Gmail
        driver.get("https://accounts.google.com/signin")
        time.sleep(2)

        driver.find_element(By.ID, "identifierId").send_keys(email + Keys.RETURN)
        time.sleep(2)
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        time.sleep(5)

        # ✅ Open YouTube Family Page
        driver.get("https://www.youtube.com/family")
        time.sleep(5)

        # ✅ Send Invitations
        for invite_email in invite_emails:
            driver.find_element(By.XPATH, "//input[@type='email']").send_keys(invite_email.strip())
            time.sleep(1)
            driver.find_element(By.XPATH, "//button[contains(text(),'Send Invitation')]").click()
            time.sleep(2)

        driver.quit()
        return jsonify({"message": "Invitations sent successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)})

# ✅ **Fixed the Syntax Error: Closing Parenthesis Added**
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)  # <-- ✅ Closing parenthesis was missing
