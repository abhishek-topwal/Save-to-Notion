import configparser
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
try:
    config.read_file(open("config.ini", "r"))
    print("Found the config file")
except FileNotFoundError as e:
    print(e)
    print("Please check if the config.ini file is in the root of project")
    sys.exit(1)



# Your LinkedIn credentials
username = config.get('LINKEDIN', 'email')
password = config.get('LINKEDIN', 'password')

driver = webdriver.Firefox()

# Navigate to the LinkedIn login page
driver.get('https://www.linkedin.com/login')

# Wait until the email field is visible
email_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'session_key')))

# Enter your email/username
email_field.send_keys(username)

# Locate the password field and enter your password
password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(password)

# Press the Enter key to submit the login form
password_field.send_keys(Keys.RETURN)

# Wait until the home page is loaded after login
WebDriverWait(driver, 10).until(EC.title_contains('LinkedIn'))

# Perform further actions on the home page if needed

# Close the browser
driver.quit()
