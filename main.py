import requests.exceptions
from json.decoder import JSONDecodeError
requests.exceptions.JSONDecodeError = JSONDecodeError

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app_store_scraper import AppStore

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('AppStore Reviews').sheet1

# Fetch App Store reviews for an app
app = AppStore(country="us", app_name="ankimobile-flashcards", app_id="373493387")
app.review(how_many=10000)  # Number of reviews to scrape

# Extract stars, text, and date for each review
reviews_data = [(review['rating'], review['review'], review['date'].isoformat()) for review in app.reviews]

# Batch write to Google Sheets (reducing the number of API write requests)
sheet.append_rows(reviews_data)

print(f"{len(reviews_data)} reviews saved to Google Sheets!")
