import requests
from bs4 import BeautifulSoup

# URL = 'https://kamernet.nl/en/for-rent/room-amsterdam'
URL = 'https://www.pararius.com/apartments/nijmegen'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Assuming that the rental cards are inside <div> elements with class "rental-card"
    # rental_cards = soup.find_all('div', id='roomAdvert_0')
    # rental_cards = soup.find_all('div', id='roomAdvert_0')
    rental_cards = soup.find_all('h2', class_='listing-search-item__title')
 
    print(f"Most recent name: {str.strip(rental_cards[0].text)}")
    # for card in rental_cards:
    #     # You can extract specific details inside the card here
    #     # For example, if there's a title inside an <h2> tag:
    #     title = card.find('h2').text
    #     print(title)
else:
    print("Failed to retrieve the web page.")