from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time

app = Flask(__name__)

def send_invites(gmail_accounts, invite_emails):
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")  # Run in headless mode
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    
    results = []
    for email, password in gmail_accounts:
        try:
            driver.get("https://accounts.google.com/signin")
            time.sleep(2)

            email_input = driver.find_element(By.ID, "identifierId")
            email_input.send_keys(email)
            email_input.send_keys(Keys.RETURN)
            time.sleep(3)

            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(5)

            driver.get("https://www.youtube.com/family")
            time.sleep(5)
            
            for invite_email in invite_emails:
                try:
                    input_box = driver.find_element(By.XPATH, "//input[@type='email']")
                    invite_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send Invite')]")
                    input_box.send_keys(invite_email)
                    invite_button.click()
                    time.sleep(3)
                    results.append(f"Invite sent to {invite_email}")
                except:
                    results.append(f"Failed to send invite to {invite_email}")
        except:
            results.append(f"Login failed for {email}")
    
    driver.quit()
    return results

@app.route("/send-invites", methods=["POST"])
def invite():
    data = request.json
    gmail_accounts = data.get("gmail_accounts", [])
    invite_emails = data.get("invite_emails", [])
    
    if not gmail_accounts or not invite_emails:
        return jsonify({"error": "Missing data"}), 400
    
    result = send_invites(gmail_accounts, invite_emails)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
