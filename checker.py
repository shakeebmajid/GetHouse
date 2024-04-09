import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import json

# from alert import send_email
from whatsapp_api_client_python import API
import os

def send_imessage(to, message):
    os.system(f"osascript send.scpt {to} '{message}' ")

# load json file
with open('green_credentials.json') as f:
    green_credentials = json.load(f)

greenAPI = API.GreenAPI(
    green_credentials["instanceId"], green_credentials["key"] 
)

# INSTRUCTIONS: download chrome webdriver and run the executable, that should be it for setup
# Set up the driver (assuming you're using Chrome)
# headless option
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(options=options)  # If chromedriver is in your PATH, you can exclude the 'executable_path' parameter

# Specify the URL you want to navigate to
URL = "https://www.pararius.com/apartments/nederland"

# load most recent name

with open("most_recent_name.txt", "r") as f:
    most_recent_name = f.read()

while True: 
    # print the time
    print(time.strftime("%H:%M:%S", time.localtime()))
    # Load the page
    driver.get(URL)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-search-item__label')))

    most_recent_card = driver.find_elements(By.CLASS_NAME, 'listing-search-item__link--title')  # Find the most recent card
    # get the inner text of the element

    print(f"Most recent card: {most_recent_card[2].text}")
    if most_recent_card[2].text != most_recent_name:
        print("New listing found")
        most_recent_name = most_recent_card[2].text
        # save most_recent_name to file
        with open("most_recent_name.txt", "w") as f:
            f.write(most_recent_name)
        
        ############ SEND EMAIL ##########
        send_imessage('shakemaj96@gmail.com', f'New Place: {most_recent_name}')
        response = greenAPI.sending.sendMessage(green_credentials["phone"] + "@c.us", f"New Place: {most_recent_name}")
        # send_email()

    # wait
    # random number between 60 and 120
    minimum = 5
    maximum = 10
    wait_time = np.random.randint(minimum * 60, maximum * 120)
    time.sleep(wait_time)

# Close the browser
driver.quit()