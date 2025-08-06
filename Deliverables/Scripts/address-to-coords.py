# This script will read the csv file containing the addresses of each dispensary, get the geolocation (lat/long), cross reference the geolocation data to determine the ZCTA of each dispensary, and append it to the dataset. 

# Imports
import os
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import requests
import time
from pathlib import Path

# Functions 
## This function will attempt to find a file within a specified directory and subdirectories. Then it will return the absolute path of that file.
def Find_File(fileName, desiredDirectory):
  try:
    for root, dirs, files in os.walk(desiredDirectory): # Search for file
      if fileName in files:
        print("File found!")
        return os.path.join(root, fileName)
    print(f"File '{fileName} not found!") # File not found output
  except FileNotFoundError:
    print(f"\nError: '{fileName}' not found.")
  except PermissionError:
    print(f"\nError: Permission for '{fileName} denied.")
  except Exception as e:
    print(f"\nError: An unknown error occured: {e}")

# MAIN
## Variables
# startDir = "C:\\Users\\micha\\Documents"     # Directory for search
# outDir = startDir + "\\GitHub\\Dispensary\\Deliverables\\Data\\"
filePath = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official' / 'Ohio-Retail-Pharmacies.csv'
outFile = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official' / 'Ohio-Retail-Pharmacies-Geo.csv'
# outPath = outDir + outFile # File Output for updated dataframe
# print(outPath)
# fileName = "06-18-2024_Ohio_Medical_Marijuana_Dispensary_Roster_COOs.csv"
# filePath = Find_File(fileName, startDir) # Joined file path
# print(f"File path: {filePath}") 

env_path = find_dotenv() # Path to .env file (in root)
load_dotenv(env_path) # Load env variables
GOOGLE_API_KEY = os.environ['GEO_API_KEY'] # API_KEY

state = "OH"
apiUrl = "https://maps.googleapis.com/maps/api/geocode/json" # Gmaps Geocoding API URL

## Read in csv
df =  pd.read_csv(filePath)

## Concatonate separate address columns and make a full address col (public address street, public address city, State, public zip)
df["Full Address"] = df['LocationStreetAddress'] + ', ' + df['LocationCity'] + ', ' + df['LocationState'] + ' ' + df['LocationZip']
print(df)

## Create new df column for geoloc data
df["Geo"] = None

## Get geloc data
### Loop through each address and request geo location data from google api (json format)
for idx, row in df.iterrows():
    address = row['Full Address']
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }
    ### data from api
    response = requests.get(apiUrl, params=params)
    data = response.json()
    # print(data)

    ### If status is ok then put the data in the appropriate index
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        df.at[idx, 'Geo'] = (location['lat'], location['lng'])
        print(df.at[idx, "Geo"])
    else:
        print(f"Geocoding failed for: {address} | Status: {data['status']}")

    time.sleep(.2)  # Wait for 1/5 of a second before next iteration

## Save df to new csv
df.to_csv(outFile, index=False)

