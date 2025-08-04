import pandas as pd
from pathlib import Path

# Load the CSV file
file_path = Path(__file__).parent.parent / 'Data' / 'Pharmacy' /'ohio-pharmacies-with-zcta.csv' 
out_file = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'ohio-pharmacies-with-zcta-split.csv'

df = pd.read_csv(file_path)

# Rename the 'Address' column to 'Full Address'
df.rename(columns={'Address': 'Full Address'}, inplace=True)

# Extract the street, city, and zip code from the full address
# Expected format: "Street, City, OH Zip, USA"
address_split = df['Full Address'].str.extract(r'^(.*?),\s*(.*?),\s*OH\s*(\d{5})')

# Assign new columns based on the extracted values
df['Public Address Street'] = address_split[0]
df['Public Address City'] = address_split[1]
df['Public Zip'] = address_split[2]

# Optionally, save the updated DataFrame to a new CSV
df.to_csv(out_file, index=False)

# Show the updated DataFrame (for interactive use)
print(df[['Full Address', 'Public Address Street', 'Public Address City', 'Public Zip']].head())
