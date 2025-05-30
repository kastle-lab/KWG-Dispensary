# This script takes in the geojson data from https://github.com/TheUpshot/presidential-precinct-map-2020 and matches the coordinate sof the dispensaries with the precint and puts the voting results into Dispensary-Roster-Geo-ZCTA.csv. 

# Imports
import geopandas as gpd
import pandas as pd
import shapely
from shapely.geometry import Point

# variables
precintFile = "./Deliverables/Data/Geo/precincts-with-results.geojson" 
rosterFile = "./Deliverables/Data/Dispensary-Roster-Geo-ZCTA.csv"
outFile = "./Deliverables/Data/Dispensary-Roster-Geo-ZCTA-Votes.csv"
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
dispVotes.drop(['PresVote','geometry','longitude', 'latitude', 'index_right'],axis=1).to_csv(outFile, index=False)