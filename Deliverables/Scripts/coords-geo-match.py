# This script takes in the geojson data from https://github.com/TheUpshot/presidential-precinct-map-2020 and matches the coordinates of the dispensaries with the precint and puts the voting results into Dispensary-Roster-Geo-ZCTA.csv. 

# Imports
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point
from pathlib import Path

# variables
precintFile = Path(__file__).parent.parent / 'Data' / 'Geo'/ 'precincts-with-results.geojson' 
rosterFile = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official' / 'Ohio-Retail-Pharmacies-with-zcta.csv'
outFile = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official' / 'Ohio-Retail-Pharmacies-with-zcta-vote.csv'

# Read files
dfGeo = gpd.read_file(precintFile)
dfRoster = pd.read_csv(rosterFile)
# print(dfGeo.columns)
# print(dfGeo.crs)

# Select desired categories
dfGeo = dfGeo[['GEOID','votes_dem', 'votes_rep', 'pct_dem_lead', 'geometry']]

# Initalize new columns and split coordinates 
dfRoster['latitude',] = None
dfRoster['longitude'] = None
dfRoster[['latitude', 'longitude']] = dfRoster['Geo'].str.strip('()').str.split(',', expand=True)

# Convert to floats for geopandas
dfRoster['latitude'] = dfRoster['latitude'].astype(float)
dfRoster['longitude'] = dfRoster['longitude'].astype(float)

# Convert coordinates reference ssytem and geometry for spatial join
geometry = [Point(xy) for xy in zip(dfRoster['longitude'], dfRoster['latitude'])]
dispGeo = gpd.GeoDataFrame(dfRoster, geometry=geometry)
dispGeo.set_crs(epsg=4326, inplace=True)
dispVotes = gpd.sjoin(dispGeo, dfGeo, how='left', predicate='within')
# print(dispVotes.head())

# Drop unnecessary columns for csv
dispVotes.drop(['geometry','longitude', 'latitude', 'index_right'],axis=1).to_csv(outFile, index=False)