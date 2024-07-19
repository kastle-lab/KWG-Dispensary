# Dispensary FIPS County Code Iterator

# Libraries
import os
import csv
import pandas as pd

# Functions
## This function is used to test the dataframes used throughout this program
def test (dataFrame):
    print("BEGIN TEST\n", dataFrame)
    print("\n",dataFrame.dtypes)
    print("\n",dataFrame.head(), "\nEND TEST\n")

## This function creates a dataframe used to store the number of dispensaries that exist in each county of Ohio
def numDispInCounty(list1, list2):
    # Declare pathing and filename
    outDir = "./Deliverables/Data"
    newFileName = "ohio-county-dispensary-qty"
    output_file = os.path.join(outDir, newFileName)

    # Sort data (A-Z)
    list1.sort()
    list2.sort()

    # Fill Dictionary / key(county):value(count)
    countyDictionary = {}
    inc = 0
    for i in list1:
        countyName=list1[inc]
        countyDictionary.update({countyName:0})
        inc = inc + 1

    # Count counties and fill values in dictionary
    for key in countyDictionary.keys():
        inc = 0
        countyCount = 0
        for i in list2:
            countyName=list2[inc]
            if (countyName == key):
                countyCount = countyCount + 1
                countyDictionary.update({key:countyCount})
            inc = inc + 1

    # Create dataframe from data
    countyDf = pd.DataFrame(countyDictionary.items(), columns=['County Name', 'Dispensary Count'])
    print(countyDf)
    print("Saving...")
    countyDf.to_csv(output_file, index=False)
    print("File saved as ", newFileName)

def transferFips(countyFipsDf, rosterDf):
    # Copy data frames
    fipsCopy = countyFipsDf.copy()
    rosCopy = rosterDf.copy()

    # Insert new column labeled FIPS in the copy of the roster data frame
    rosCopy["FIPS"] = 0
    
    # Iterate through both data frames and find matches for counties and insert FIPS code into the copy of the roster data frame

# Main
## File inputs
rosterDf = pd.read_csv("Deliverables/Data/06-18-2024_Ohio_Medical_Marijuana_Dispensary_Roster_COOs.csv")
countyFipsDf = pd.read_csv("Deliverables/Data/ohio-county-fips2.csv")
countyDataDf = pd.read_csv("Deliverables/Data/Ohio_County_Data.csv")

## Create Lists
countyList = list(countyFipsDf["County"])
fipsList = list(countyFipsDf["FIPS"])
counties = rosterDf['Public Address - County']
countiesList = counties.tolist()

## Perform function for counting the number of dispensaries in a county
# numDispInCounty(countyList,countiesList)  # count the number of dispensaries in ea county

## Perform Function for adding FIPS codes from countyFIPS to roster file.
# transferFips(countyFipsDf, rosterDf)

# print(rosterDf.loc[:,"Public Address - County"])
# print(countyDataDf.co_fip)

## File Checks
# test(rosterDf)
# test(countyFipsDf)
# test(countyDataDf)
