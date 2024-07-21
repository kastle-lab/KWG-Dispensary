# Dispensary FIPS County Code Iterator

# Libraries
import os
import csv
import pandas as pd
import numpy as np

# Functions
## This function is used to test the dataframes used throughout this program
def test (dataFrame):
    print("BEGIN TEST\n", dataFrame)
    print("\n",dataFrame.dtypes)
    print("\nEND TEST\n")

# This function will save a data frame to the desired directory with the desired filename.
def saveDataFrame(df, dir, fName):
    # Declare pathing and filename
    outDir = dir
    newFileName = fName
    output_file = os.path.join(outDir, newFileName)

    # Save file as csv
    print("Saving...")
    df.to_csv(output_file, index=False)
    print("File saved as ", newFileName)
    print(df)

# This function will find matches between two data frames (df), compare items in the specified columns for each df, and fill them into df2 that is returned.
def matchInsert(df1, df2, mapColName1, mapColName2, colNameMatch, newColName):
    # Copy data frames
    df1Copy = df1.copy()
    df2Copy = df2.copy()

    # Create new column in df2
    df2Copy[newColName] = 0

    # Create a mapping from mapColName1 to mapColName2
    fipsMap = dict(zip(df1Copy[mapColName1], df1Copy[mapColName2]))

    # Map the newColName values based on colNameMatch using the map
    df2Copy[newColName] = df2Copy[colNameMatch].map(fipsMap)

    # If data type is numeric, replace NaN's with 0 and convert values to integer (removes decimals)
    if pd.api.types.is_numeric_dtype(df2Copy[newColName]):
        df2Copy[newColName] = df2Copy[newColName].fillna(0).astype(int)

    print(df2Copy)
    return df2Copy

# Main
## File inputs
rosterDf = pd.read_csv("./Deliverables/Data/06-18-2024_Ohio_Medical_Marijuana_Dispensary_Roster_COOs.csv")
countyFipsDf = pd.read_csv("./Deliverables/Data/ohio-county-fips.csv")
countyDataDf = pd.read_csv("./Deliverables/Data/Ohio_County_Data.csv")

# count the number of dispensaries in ea county and save
dispensaryCountyQtySeries = rosterDf['Public Address - County'].value_counts()
dispensaryCountyQtyDf = dispensaryCountyQtySeries.reset_index()
dispensaryCountyQtyDf.columns = ['County', 'Count']
saveDataFrame(dispensaryCountyQtyDf, "./Deliverables/Data","ohio-county-dispensary-qty")

# match fips code with county in rosterDf
newRosDf = matchInsert(countyFipsDf, rosterDf, "label", "fips", "Public Address - County", "Fips")
saveDataFrame(newRosDf,"./Deliverables/Data","Roster-fips.csv")

## File Checks
# test(rosterDf)
# test(countyFipsDf)
# test(countyDataDf)
