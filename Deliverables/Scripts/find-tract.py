import pandas as pd
import requests
import time
import json
from typing import Optional, Tuple
from pathlib import Path

def parse_coordinates(geo_string: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Parse latitude and longitude from a coordinate string.
    
    Args:
        geo_string (str): Coordinate string in format 'lat,lon'
    
    Returns:
        Tuple[Optional[float], Optional[float]]: (latitude, longitude) or (None, None) if parsing fails
    """
    try:
        if pd.isna(geo_string) or geo_string == '':
            return None, None
        
        coords = str(geo_string).strip().split(',')
        if len(coords) != 2:
            return None, None
        
        lat = float(coords[0].strip())
        lon = float(coords[1].strip())
        
        # Basic validation for reasonable coordinate ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        else:
            return None, None
            
    except (ValueError, AttributeError, IndexError):
        return None, None

def get_tract_code_from_fcc(latitude: float, longitude: float, timeout: int = 10) -> Optional[str]:
    """
    Get census tract code from FCC API using coordinates.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        timeout (int): Request timeout in seconds
    
    Returns:
        Optional[str]: Census tract code or None if request fails
    """
    
    # FCC Block API endpoint
    url = "https://geo.fcc.gov/api/census/area"
    
    params = {
        'lat': latitude,
        'lon': longitude,
        'censusYear': '2020',  # Use 2020 census data
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract tract code from the response
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            if result['block_fips']:
                # Census tract is the first 11 digits of the block FIPS code
                # Format: SS CCC TTTTTT BBBB (State, County, Tract, Block)
                block_fips = result['block_fips']
                if len(block_fips) >= 11:
                    tract_code = block_fips[:11]  # First 11 digits = state + county + tract
                    return tract_code
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request error for coordinates ({latitude}, {longitude}): {e}")
        return None
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Data parsing error for coordinates ({latitude}, {longitude}): {e}")
        return None

def add_tract_codes_to_csv(input_file: str, output_file: str, delay: float = 0.1):
    """
    Add census tract codes to a CSV file using FCC API.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        delay (float): Delay between API calls in seconds to be respectful
    """
    
    print(f"Reading CSV file: {input_file}")
    
    # Read the CSV file
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Check if 'Geo' column exists
    if 'Geo' not in df.columns:
        print("Error: 'Geo' column not found in CSV file")
        print(f"Available columns: {list(df.columns)}")
        return
    
    # Add new column for tract codes
    df['Census_Tract_Code'] = None
    
    # Track statistics
    total_rows = len(df)
    successful_lookups = 0
    failed_lookups = 0
    invalid_coordinates = 0
    
    print(f"Processing {total_rows} rows...")
    
    # Process each row
    for idx, row in df.iterrows():
        geo_value = row['Geo']
        
        # Parse coordinates
        lat, lon = parse_coordinates(geo_value.strip('()'))
        
        if lat is None or lon is None:
            print(f"Row {idx + 1}: Invalid coordinates format: '{geo_value}'")
            invalid_coordinates += 1
            continue
        
        print(f"Row {idx + 1}: Looking up tract for coordinates ({lat}, {lon})")
        
        # Get tract code from FCC API
        tract_code = get_tract_code_from_fcc(lat, lon)
        
        if tract_code:
            df.loc[idx, 'Census_Tract_Code'] = tract_code
            successful_lookups += 1
            print(f"  -> Found tract code: {tract_code}")
        else:
            failed_lookups += 1
            print(f"  -> Failed to get tract code")
        
        # Add delay to be respectful to the API
        if delay > 0:
            time.sleep(delay)
    
    # Save the updated dataframe
    print(f"\nSaving results to: {output_file}")
    try:
        df.to_csv(output_file, index=False)
        print("File saved successfully!")
    except Exception as e:
        print(f"Error saving file: {e}")
        return
    
    # Print summary statistics
    print(f"\n=== SUMMARY ===")
    print(f"Total rows processed: {total_rows}")
    print(f"Successful tract lookups: {successful_lookups}")
    print(f"Failed tract lookups: {failed_lookups}")
    print(f"Invalid coordinate formats: {invalid_coordinates}")
    print(f"Success rate: {successful_lookups/total_rows*100:.1f}%")

def test_single_coordinate(latitude: float, longitude: float):
    """
    Test the FCC API with a single coordinate pair.
    
    Args:
        latitude (float): Test latitude
        longitude (float): Test longitude
    """
    print(f"Testing FCC API with coordinates: ({latitude}, {longitude})")
    
    tract_code = get_tract_code_from_fcc(latitude, longitude)
    
    if tract_code:
        print(f"Success! Tract code: {tract_code}")
        # Parse the tract code components
        state_code = tract_code[:2]
        county_code = tract_code[2:5]
        tract_code_part = tract_code[5:11]
        print(f"  State: {state_code}")
        print(f"  County: {county_code}")
        print(f"  Tract: {tract_code_part}")
    else:
        print("Failed to get tract code")

# Example usage
if __name__ == "__main__":
    # Test with the example coordinates you provided
    print("Testing with example coordinates...")
    test_single_coordinate(38.7318162, -82.99715180000001)
    print("\n" + "="*50 + "\n")
    
    # Process CSV file
    input_file = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official'/'Ohio-Retail-Pharmacies-with-zcta-vote-ins-hh.csv' 
    output_file = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official'/'Ohio-Retail-Pharmacies-with-zcta-vote-ins-hh-tract.csv' 
    
    # Add a small delay between requests to be respectful to the FCC API
    api_delay = 0.1  # 100ms delay between requests
    
    try:
        add_tract_codes_to_csv(input_file, output_file, delay=api_delay)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")