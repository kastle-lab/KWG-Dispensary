# This script uses the google places api to acquire the location data for pharmacy locations in the state of Ohio. 

# Imports
from dotenv import find_dotenv, load_dotenv
import os
import requests

# Functions

# Variables
statePlaceId = "ChIJwY5NtXrpNogRFtmfnDlkzeU"
types = ["pharmacy", "drugstore"]
apiUrl = "https://areainsights.googleapis.com/v1:computeInsights"

### MAIN ### 
env_path = find_dotenv() # Path to .env file (in root)
load_dotenv(env_path) # Load env variables
GOOGLE_API_KEY = os.environ['GEO_API_KEY'] # API_KEY
params = {
    "key": GOOGLE_API_KEY
}
r = requests.post(apiUrl, data={'key': 'value'}, params=params)
data = r.json()
print(data)