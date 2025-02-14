from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening browser
    driver = webdriver.Chrome(options=options)
    return driver

def login_and_invite(email, password, invite_emails):
    driver = get_driver()
    try:
        driver.get("https://accounts.google.com/signin")
        time.sleep(3)

        driver.find_element(By.ID, "identifierId").send_keys(email, Keys.RETURN)
        time.sleep(3)
        driver.find_element(By.NAME, "Passwd").send_keys(password, Keys.RETURN)
        time.sleep(5)

        driver.get("https://www.youtube.com/family")
        time.sleep(5)

        invite_button = driver.find_element(By.XPATH, '//button[contains(text(), "Invite family members")]')
        invite_button.click()
        time.sleep(3)

        for invite_email in invite_emails:
            email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
            email_input.send_keys(invite_email, Keys.RETURN)
            time.sleep(2)

        driver.find_element(By.XPATH, '//button[contains(text(), "Send invitations")]').click()
        time.sleep(2)
        return "Invitations sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        driver.quit()

@app.route('/')
def home():
    return "YouTube Family Invitation Bot is Running!"

@app.route('/invite', methods=['POST'])
def invite():
    data = request.json
    email = data['email']
    password = data['password']
    invite_emails = data['inviteEmails'].split("\n")
    result = login_and_invite(email, password, invite_emails)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)
