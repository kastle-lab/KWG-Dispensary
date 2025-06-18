# This script uses the google places api to acquire the location data for pharmacy locations in the state of Ohio. 

# Imports
from dotenv import find_dotenv, load_dotenv
import os
import requests
import json
import pandas as pd
import time

# Functions

# Variables
env_path = find_dotenv() # Path to .env file (in root)
load_dotenv(env_path) # Load env variables
GOOGLE_API_KEY = os.environ['GEO_API_KEY'] # API_KEY

query = "Pharmacies in Ohio"
url = "https://places.googleapis.com/v1/places:searchText"

columnHeaders = ['Business_Name', 'Address', 'Geo', 'Operational_Status','Places_ID']
df = pd.DataFrame(columns=columnHeaders)

params = {
  "key": GOOGLE_API_KEY,
  "textQuery": query,
  "fields": "places.displayName,places.businessStatus,places.formattedAddress,places.businessStatus,places.location,places.id,nextPageToken",
  "includedType":"pharmacy"
}

### MAIN ### 
r = requests.post(url, params=params)

if r.status_code == 200:
  data = r.json()
else:
  print(f"Failed to retrieve data {r.status_code}\n{r.text}")

places = data['places']
for place in places:
  placeId = place['id']
  placeLocation = place['location']
  placeLat = placeLocation['latitude']
  placeLon = placeLocation['longitude']
  displayName = place['displayName']
  placeName = displayName['text']

nextPageToken = data["nextPageToken"]

