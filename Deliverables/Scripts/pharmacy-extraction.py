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

params = {
  "key": GOOGLE_API_KEY,
  "textQuery": query,
  "fields": "places.displayName,places.formattedAddress,places.businessStatus,places.location,places.id,nextPageToken",
  "includedType":"pharmacy"
}

### MAIN ### 
r = requests.post(url, params=params)

if r.status_code == 200:
  data = r.json()
else:
  print(f"Failed to retrieve data {r.status_code}\n{r.text}")
  
nextPageToken = data["nextPageToken"]

print(json.dumps(data, indent=2))

