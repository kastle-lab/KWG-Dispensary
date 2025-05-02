import requests
import pandas as pd
import json
import time
from pathlib import Path

# MAIN
## Variables
inFile = Path(__file__).parent.parent / 'Data' / 'Dispensary-Roster-Geo.csv'
outFile = Path(__file__).parent.parent / 'Data' / 'Dispensary-Roster-Geo-ZCTA.csv' 
url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates" # U.S. Census API Url for coordinates

## Read in csv an create new col for ZCTA
df =  pd.read_csv(inFile)
df["ZCTA5"] = None

## Iterate through each row, create varibles from geocoordinates, request ZCTA data from U.S. Census API, and append to dataframe
for idx, row in df.iterrows():
  ### Split coordinates into variables
  coord = df.iloc[idx]["Geo"].strip('()').split(',')
  lat = float(coord[0])
  lon = float(coord[1])

  parameters = {
    "x": lon,
    "y": lat,
    "benchmark": "Public_AR_Current",       # current census geography
    "vintage": "Current_Current",        # current vintage
    "format": "json",
    "layers": "2"   # Data Layer (2 for ZCTA)
  }

  r = requests.get(url, params=parameters)
  data = r.json()
  # print(json.dumps(data, indent=2))

  try:
    zcta = data["result"]["geographies"]["2020 Census ZIP Code Tabulation Areas"][0]["ZCTA5"]
    df.at[idx,'ZCTA5'] = zcta
    # print(df.at[idx,'ZCTA5'])
  except: 
    print(f"ZCTA ${zcta} not found!")

  time.sleep(.2)  # Wait for 1/5 of a second before next iteration

  # print(idx, ': ', lat, lon)

df.to_csv(outFile, index=False)
