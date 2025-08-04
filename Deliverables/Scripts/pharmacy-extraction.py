# Imports
from dotenv import find_dotenv, load_dotenv
import os
import requests
import json
import pandas as pd
import time
import math

# Functions
def extract_place_data(place):
    """Extract relevant data from a place object"""
    try:
        place_id = place.get('id', '')
        
        # Extract location coordinates
        location = place.get('location', {})
        lat = location.get('latitude', '')
        lon = location.get('longitude', '')
        geo_coords = f"{lat},{lon}" if lat and lon else ''
        
        # Extract display name
        display_name = place.get('displayName', {})
        business_name = display_name.get('text', '') if display_name else ''
        
        # Extract address
        address = place.get('formattedAddress', '')
        
        # Extract business status
        operational_status = place.get('businessStatus', '')
        
        return {
            'Business_Name': business_name,
            'Address': address,
            'Geo': geo_coords,
            'Operational_Status': operational_status,
            'Places_ID': place_id
        }
    except Exception as e:
        print(f"Error extracting place data: {e}")
        return None

def make_api_request(url, headers, payload, max_retries=3):
    """Make API request with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit exceeded
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"API request failed with status {response.status_code}: {response.text}")
                if attempt == max_retries - 1:
                    return None
        except Exception as e:
            print(f"Request error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    
    return None

def generate_ohio_grid(grid_size_miles=25):
    """Generate a grid of search points covering Ohio"""
    # Ohio boundaries (approximate)
    ohio_bounds = {
        'north': 41.977,
        'south': 38.403,
        'east': -80.519,
        'west': -84.820
    }
    
    # Convert miles to degrees (approximate)
    # 1 degree latitude ≈ 69 miles
    # 1 degree longitude ≈ 69 * cos(latitude) miles
    lat_step = grid_size_miles / 69.0
    
    grid_points = []
    current_lat = ohio_bounds['south']
    
    while current_lat <= ohio_bounds['north']:
        # Calculate longitude step based on current latitude
        lon_step = grid_size_miles / (69.0 * math.cos(math.radians(current_lat)))
        current_lon = ohio_bounds['west']
        
        while current_lon <= ohio_bounds['east']:
            grid_points.append({
                'latitude': current_lat,
                'longitude': current_lon
            })
            current_lon += lon_step
        
        current_lat += lat_step
    
    return grid_points

def search_around_point(url, headers, lat, lon, radius_meters=40000):
    """Search for pharmacies around a specific point"""
    payload = {
        "textQuery": "pharmacy",
        "includedType": "pharmacy",
        "maxResultCount": 20,
        "locationBias": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},
                "radius": radius_meters
            }
        }
    }
    
    all_places = []
    next_page_token = None
    page_count = 0
    
    while True:
        page_count += 1
        
        # Add nextPageToken if available
        if next_page_token:
            payload["pageToken"] = next_page_token
        elif "pageToken" in payload:
            del payload["pageToken"]
        
        # Make API request
        data = make_api_request(url, headers, payload)
        
        if not data:
            break
        
        # Process places from current page
        places = data.get('places', [])
        all_places.extend(places)
        
        # Check for next page token
        next_page_token = data.get("nextPageToken")
        
        if not next_page_token or page_count >= 3:  # Limit pages per point to control API usage
            break
        
        # Small delay between page requests
        time.sleep(1)
    
    return all_places

def is_in_ohio(lat, lon):
    """Check if coordinates are within Ohio boundaries (approximate)"""
    ohio_bounds = {
        'north': 41.977,
        'south': 38.403,
        'east': -80.519,
        'west': -84.820
    }
    
    return (ohio_bounds['south'] <= lat <= ohio_bounds['north'] and 
            ohio_bounds['west'] <= lon <= ohio_bounds['east'])

# Variables
env_path = find_dotenv()  # Path to .env file (in root)
load_dotenv(env_path)  # Load env variables
GOOGLE_API_KEY = os.environ['GEO_API_KEY']  # API_KEY

# API configuration
url = "https://places.googleapis.com/v1/places:searchText"

headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': GOOGLE_API_KEY,
    'X-Goog-FieldMask': 'places.displayName,places.businessStatus,places.formattedAddress,places.location,places.id,nextPageToken'
}

columnHeaders = ['Business_Name', 'Address', 'Geo', 'Operational_Status', 'Places_ID']
df = pd.DataFrame(columns=columnHeaders)

### MAIN ###
print("Starting comprehensive pharmacy data collection for Ohio...")
print("Using grid-based search strategy to cover the entire state...")

# Generate search grid
grid_points = generate_ohio_grid(grid_size_miles=25)  # 25-mile grid
print(f"Generated {len(grid_points)} search points across Ohio")

# Track unique places using Places_ID
unique_places = set()
all_pharmacy_data = []
grid_point_count = 0
total_api_calls = 0

# Search around each grid point
for point in grid_points:
    grid_point_count += 1
    lat, lon = point['latitude'], point['longitude']
    
    print(f"Searching grid point {grid_point_count}/{len(grid_points)} "
          f"(Lat: {lat:.3f}, Lon: {lon:.3f})")
    
    # Search for pharmacies around this point
    places = search_around_point(url, headers, lat, lon, radius_meters=40000)  # ~25 mile radius
    total_api_calls += 1
    
    new_places_count = 0
    for place in places:
        place_data = extract_place_data(place)
        
        if place_data and place_data['Places_ID']:
            # Check if this is a new unique place
            if place_data['Places_ID'] not in unique_places:
                # Verify the place is actually in Ohio
                if place_data['Geo']:
                    try:
                        place_lat, place_lon = map(float, place_data['Geo'].split(','))
                        if is_in_ohio(place_lat, place_lon):
                            unique_places.add(place_data['Places_ID'])
                            all_pharmacy_data.append(place_data)
                            new_places_count += 1
                    except ValueError:
                        continue
    
    print(f"  Found {len(places)} total places, {new_places_count} new unique Ohio pharmacies")
    print(f"  Running total: {len(all_pharmacy_data)} unique pharmacies")
    
    # Rate limiting - wait between grid points
    if grid_point_count % 5 == 0:  # Longer pause every 5 points
        print("  Taking a longer break to respect API limits...")
        time.sleep(5)
    else:
        time.sleep(2)

# Convert to DataFrame
if all_pharmacy_data:
    df = pd.DataFrame(all_pharmacy_data)
else:
    print("No pharmacy data collected!")

# Final results
print(f"\n=== COLLECTION COMPLETE ===")
print(f"Grid points searched: {len(grid_points)}")
print(f"Total API calls made: {total_api_calls}")
print(f"Unique pharmacies found: {len(all_pharmacy_data)}")
print(f"DataFrame shape: {df.shape}")

if not df.empty:
    # Display first few rows
    print("\nFirst 5 results:")
    print(df.head())

    # Save to CSV
    output_filename = "ohio-pharmacies.csv"
    df.to_csv(output_filename, index=False)
    print(f"\nData saved to {output_filename}")

    # Display statistics
    print(f"\nSummary Statistics:")
    print(f"- Total unique pharmacies: {len(df)}")
    if 'Operational_Status' in df.columns:
        status_counts = df['Operational_Status'].value_counts()
        for status, count in status_counts.items():
            print(f"- {status}: {count}")

    # Sample of cities found
    if 'Address' in df.columns:
        print(f"\nSample cities found:")
        cities = df['Address'].str.extract(r', ([^,]+), OH')[0].value_counts().head(10)
        for city, count in cities.items():
            if pd.notna(city):
                print(f"- {city}: {count} pharmacies")

print("\nScript execution completed!")