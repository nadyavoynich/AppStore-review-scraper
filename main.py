import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app_store_scraper import AppStore

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open('AppStore Reviews').sheet1

# Fetch App Store reviews for AnkiDroid app
app = AppStore(country="us", app_name="ankidroid-flashcards", app_id="1237663323")  # Use actual app_name and app_id for AnkiDroid
app.review(how_many=1000)  # Number of reviews you want to scrape

# Extract stars, text, and date for each review
reviews_data = [(review['rating'], review['review'], review['date']) for review in app.reviews]

# Batch write to Google Sheets (reducing the number of API write requests)
sheet.append_rows(reviews_data)

print(f"{len(reviews_data)} reviews saved to Google Sheets!")
