# This script will read the csv file containing the addresses of each dispensary, get the geolocation (lat/long), and append it to the dataset. 

# Imports
import os
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import googlemaps

# Functions 

# This function will attempt to find a file within a specified directory and subdirectories. Then it will return the absolute path of that file.
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
start_dir = "C:\\Users\\micha\\Documents"     # Directory 
fileName = "06-18-2024_Ohio_Medical_Marijuana_Dispensary_Roster_COOs.csv"
filePath = Find_File(fileName, start_dir) # Joined file path
# print(f"File path: {filePath}") 

env_path = find_dotenv() # Path to .env file
load_dotenv(env_path) # Load env variables
GOOGLE_API_KEY = os.environ['GEO_API_KEY'] # API_KEY

state = "OH"

# Read in csv
df =  pd.read_csv(filePath)

# get address from columns and make into a variable (public address street, public address city, State, public zip)
df["Full Address"] = df['Public Address Street'] + ' ' + df['Public Address City'] + ', ' + state + ' ' + df['Public Zip']

# get geloc data
print(df)
# append geloc data