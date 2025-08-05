import pandas as pd
from pathlib import Path

# File paths
roster_path = Path(__file__).parent.parent / 'Data' /'Primary-Dataset-2(pharmacy).csv' 
insured_path = Path(__file__).parent.parent / 'Data' / 'ZCTA' / 'ACSST5Y2023-health-insurance-coverage-zcta.csv'
output_path = Path(__file__).parent.parent / 'Data' /'Primary-Dataset-2(pharmacy)-NEW.csv' 

# Load data
dfRoster = pd.read_csv(roster_path)
dfInsured = pd.read_csv(insured_path)

# Prepare new columns
dfRoster["TotalPop"] = None
dfRoster["PopInsured"] = None

# Build a lookup dictionary from dfInsured's single row
insured_row = dfInsured.iloc[0]
zcta_lookup = {}

for col in insured_row.index:
    if "!!Total!!Estimate" in col:
        zcta = col.split("!!")[0].split()[1]  # Extract ZCTA5 code
        zcta_lookup[zcta] = {
            "Total": insured_row[col],
            "Insured": None  # Will fill in next
        }

for col in insured_row.index:
    if "!!Insured!!Estimate" in col:
        zcta = col.split("!!")[0].split()[1]
        if zcta in zcta_lookup:
            zcta_lookup[zcta]["Insured"] = insured_row[col]

# Fill in values to dfRoster
for i, row in dfRoster.iterrows():
    zcta = str(row["ZCTA5"]).zfill(5)  # Ensure 5-digit format
    if zcta in zcta_lookup:
        dfRoster.at[i, "TotalPop"] = zcta_lookup[zcta]["Total"]
        dfRoster.at[i, "PopInsured"] = zcta_lookup[zcta]["Insured"]

# Save to CSV
dfRoster.to_csv(output_path, index=False)

print(dfRoster[['ZCTA5', 'TotalPop', 'PopInsured']])
