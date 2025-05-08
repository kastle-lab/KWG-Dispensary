# This script uses Pandas to grab data from the ZCTA data on health-insurance-coverge, add it to a dataframe consisting of the data from Dispensary-Roster-Geo-ZCTA, and save it to that file. 
import pandas as pd
import time 

### MAIN ###
# Variables
zctaNum = ""
rowPop = 'Civilian noninstitutionalized population'

# Read in csvs and create new columns
outFile = "./Deliverables/Data/Dispensary-Roster-Geo-ZCTA-New.csv"
dfRoster = pd.read_csv("./Deliverables/Data/Dispensary-Roster-Geo-ZCTA.csv")
dfInsured = pd.read_csv("./Deliverables/Data/ZCTA/ACSST5Y2023-health-insurance-coverage-zcta.csv")
dfRoster["TotalPop"] = None
dfRoster["PopInsured"] = None

# Get zcta code from row dfRoster
rosterZctas = dfRoster['ZCTA5']

# Create new df with only data
newDf = dfInsured.iloc[[0]]

# Match with dfInsured col label (ZCTA5 43001!!Total!!Estimate,ZCTA5 43001!!Insured!!Estimate ) and join with dfRoster
count = 0

for col in newDf:
    for zcta in rosterZctas:
            zctaNum = zcta
            labelTotal = f'ZCTA5 {zctaNum}!!Total!!Estimate'
            labelIns = f'ZCTA5 {zctaNum}!!Insured!!Estimate'

            if col == labelTotal:
                # print(newDf[col])
                dfRoster.loc[count, 'TotalPop'] = newDf.at[0, col]
                # time.sleep(2)

            if col == labelIns:
                #  print(newDf[col])
                 dfRoster.loc[count, 'PopInsured'] = newDf.at[0, col]
                #  time.sleep(2)
    count = count + 1

print(dfRoster[['TotalPop', 'PopInsured']])

dfRoster.to_csv(outFile, index=False)
