import time
import base64
import requests
import getpass
import smtplib
import pickle
from requests import HTTPError
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
# flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
# creds = flow.run_local_server(port=0)
# service = build('gmail', 'v1', credentials=creds)



NUM_MINUTES = 1
URL = 'https://www.pararius.com/apartments/nijmegen'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

two_br_message = "Dear agent, \n\
\n\
This is Andrea Russo; I am a master student in physics and astronomy at Radboud university. \n\
Together with a colleague of mine we were looking to rent an apartment for the upcoming year, and this caught our interest. \n\
We're orderly and tidy people, and we are looking for a quiet accommodation to finish our studies. \n\
Alongside university, we both have part time jobs to sustain ourselves. \n\
\n\
I'm looking forward to hearing back from you about the property, it's really lovely! \n\
\n\
Kind regards, \n\
Andrea"


# check page
# TODO: load from pickle
last_most_recent_listing = "Flat Einsteinstraat"
with open('most_recent_listing.pickle', 'rb') as f:
    last_most_recent_listing = pickle.load(f)
    
print(f"############# Last most recent listing: {last_most_recent_listing} #############")
while True:
    time.sleep(NUM_MINUTES * 60)
    response = requests.get(URL, headers=HEADERS)
    print("Checking page...")
    print(f"Last most recent listing: {last_most_recent_listing}")
    print(f"TIME: {time.strftime('%H:%M:%S', time.localtime())}")

    # ########## SEND EMAIL ##########
    # print("Sending email...")
    # message = MIMEText('Hi! I am a robot and this is a test.')
    # message['to'] = 'shakemaj96@gmail.com'
    # message['subject'] = 'Test Email'
    # create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    # try:
    #     message = (service.users().messages().send(userId="me", body=create_message).execute())
    #     print(F'sent message to {message} Message Id: {message["id"]}')
    # except HTTPError as error:
    #     print(F'An error occurred: {error}')
    #     message = None
    # print("Email sent!")
    # ################################
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Assuming that the rental cards are inside <div> elements with class "rental-card"
        # rental_cards = soup.find_all('div', id='roomAdvert_0')
        # rental_cards = soup.find_all('div', id='roomAdvert_0')
        rental_cards = soup.find_all('h2', class_='listing-search-item__title')
    
        print(f"Most recent name: {str.strip(rental_cards[0].text)}")
        most_recent_listing = str.strip(rental_cards[0].text)
        if most_recent_listing != last_most_recent_listing:
            last_most_recent_listing = most_recent_listing
            # TODO: save most recent to pickle
            with open('most_recent_listing.pickle', 'wb') as f:
                pickle.dump(most_recent_listing, f)
            

            print("New listing found!")
            # Set up the driver (assuming you're using Chrome)
            driver = webdriver.Chrome()  # If chromedriver is in your PATH, you can exclude the 'executable_path' parameter
            driver.get(URL)  # Load the page

            # TODO: find all new elements instead of just one
            # all_recent_listings = driver.find_elements(By.CLASS_NAME, 'search-list__item--listing')
            # print(f"Number of recent listings: {len(all_recent_listings)}")

            most_recent_card = driver.find_element(By.CLASS_NAME, 'search-list__item--listing')  # Find the most recent card
            img_sub_element = most_recent_card.find_element(By.TAG_NAME, 'img')  # Find the img sub-element
            img_sub_element.click()  # Click on the img sub-element

            # check how many bedrooms 
            bedroom_div = driver.find_element(By.CLASS_NAME, 'listing-features__description--number_of_bedrooms')
            # get span element
            bedroom_span = bedroom_div.find_element(By.TAG_NAME, 'span')
            # get text
            num_bedrooms = int(bedroom_span.text)

            # click to contact agent
            contact_element = driver.find_element(By.CLASS_NAME, "agent-summary__agent-contact-request")
            driver.execute_script("arguments[0].click()", contact_element)

            print(f"Number of bedrooms: {num_bedrooms}")
            # check number of bedrooms and fill form accordingly
            if num_bedrooms == 1:
                print("1 bedroom")
                input_field = driver.find_element(By.NAME, "listing_contact_agent_form[message]")
                input_field.send_keys('Hi I am interested in a house to rent. Please contact me.')
            elif num_bedrooms == 2:
                print("2 bedrooms")
                input_field = driver.find_element(By.NAME, "listing_contact_agent_form[message]")
                input_field.send_keys(two_br_message)
            else:
                print("More than 2 bedrooms")
                continue

            first_name = "Andrea"
            last_name = "Russo"
            email = "andrea-15@virgilio.it"

            first_name_element = driver.find_element(By.CLASS_NAME, "form__first-name")

            first_name_element.find_element(By.TAG_NAME, "input").send_keys(first_name)

            last_name_element = driver.find_element(By.CLASS_NAME, "form__last-name")

            last_name_element.find_element(By.TAG_NAME, "input").send_keys(last_name)

            email_element = driver.find_element(By.CLASS_NAME, "form__email")

            email_element.find_element(By.TAG_NAME, "input").send_keys(email)
            
            phone_element = driver.find_element(By.CLASS_NAME, "form__phone")

            phone_element.find_element(By.TAG_NAME, "input").send_keys ('+31612345678')

           
            # get button element
            send_button = driver.find_element(By.CLASS_NAME, "form__buttons") 

            # DONT CLICK IT UNLESS LIVE
            if num_bedrooms == 2: 
                driver.execute_script("arguments[0].click()", send_button.find_element(By.TAG_NAME, "button"))
                print("2 bedrooms!")

        else:
            print("No new listing found.")

    else:
        print("Failed to retrieve the web page.")

    # TEST PURPOSES ONLY
    # time.sleep(NUM_MINUTES * 60)