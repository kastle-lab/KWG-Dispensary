# Dispensary FIPS County Code Iterator

# Libraries
import os
import csv
import pandas as pd
import numpy as np

# Functions
## This function is used to test the data_frames used throughout this program
def test (data_frame):
    print("BEGIN TEST\n", data_frame)
    print("\n",data_frame.dtypes)
    print("\nEND TEST\n")

# This function will save a data frame to the desired directory with the desired filename.
def save_data_frame(df, dir, file_name):
    # Declare pathing and filename
    output_directory = dir
    new_file_name = file_name
    output_file = os.path.join(output_directory, new_file_name)

    # Save file as csv
    print("Saving...")
    df.to_csv(output_file, index=False)
    print("File saved as ", new_file_name)
    print(df)

# This function will find matches between two data frames (df), compare items in the specified columns for each df, and fill them into df2 that is returned.
def match_insert(df1, df2, map_col_name1, map_col_name2, col_name_match, new_col_name):
    # Copy data frames
    df1_copy = df1.copy()
    df2_copy = df2.copy()

    # Create new column in df2
    df2_copy[new_col_name] = 0

    # Create a mapping from map_col_name1 to map_col_name2
    fipsMap = dict(zip(df1_copy[map_col_name1], df1_copy[map_col_name2]))

    # Map the new_col_name values based on col_name_match using the map
    df2_copy[new_col_name] = df2_copy[col_name_match].map(fipsMap)

    # If data type is numeric, replace NaN's with 0 and convert values to integer (removes decimals)
    if pd.api.types.is_numeric_dtype(df2_copy[new_col_name]):
        df2_copy[new_col_name] = df2_copy[new_col_name].fillna(0).astype(int)

    print(df2_copy)
    return df2_copy

# Main
## File inputs
df_roster = pd.read_csv("./Deliverables/Data/06-18-2024_Ohio_Medical_Marijuana_Dispensary_Roster_COOs.csv")
df_county_fips = pd.read_csv("./Deliverables/Data/ohio-county-fips.csv")
df_county_data = pd.read_csv("./Deliverables/Data/Ohio_County_Data.csv")

# count the number of dispensaries in ea county and save
dispensary_county_quantity_series = df_roster['Public Address - County'].value_counts()
df_dispensary_county_qty = dispensary_county_quantity_series.reset_index()
df_dispensary_county_qty.columns = ['County', 'Count']
save_data_frame(df_dispensary_county_qty, "./Deliverables/Data","ohio-county-dispensary-qty")

# match fips code with county in df_roster
df_new_roster = match_insert(df_county_fips, df_roster, "label", "fips", "Public Address - County", "Fips")
save_data_frame(df_new_roster,"./Deliverables/Data","roster-fips.csv")

## File Checks
# test(df_roster)
# test(df_county_fips)
# test(df_county_data)
