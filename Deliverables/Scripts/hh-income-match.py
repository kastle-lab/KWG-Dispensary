import pandas as pd
import re
from pathlib import Path

def merge_income_data(file1_path, file2_path, output_path):
    """
    Merge income data from two CSV files based on ZCTA5 matching.
    
    Args:
        file1_path (str): Path to the first CSV file with ZCTA5 column
        file2_path (str): Path to the second CSV file with income data
        output_path (str): Path for the output merged CSV file
    """
    
    # Read the first CSV file
    print("Reading first CSV file...")
    df1 = pd.read_csv(file1_path)
    
    # Read the second CSV file
    print("Reading second CSV file...")
    df2 = pd.read_csv(file2_path)
    
    # Check if ZCTA5 column exists in first file
    if 'ZCTA5' not in df1.columns:
        raise ValueError("Column 'ZCTA5' not found in first CSV file")
    
    # Find columns in the second file that match the ZCTA5 pattern
    zcta5_pattern = re.compile(r'ZCTA5 (\d{5})!!Households!!Estimate')
    zcta5_columns = []
    zcta5_codes = []
    
    for col in df2.columns:
        match = zcta5_pattern.match(col)
        if match:
            zcta5_columns.append(col)
            zcta5_codes.append(match.group(1))
    
    print(f"Found {len(zcta5_columns)} ZCTA5 columns in second file")
    
    # Find the rows containing median and mean income data
    median_income_row = None
    mean_income_row = None
    
    for idx, row in df2.iterrows():
        if 'Median income (dollars)' in str(row.iloc[0]):
            median_income_row = idx
        elif 'Mean income (dollars)' in str(row.iloc[0]):
            mean_income_row = idx
    
    if median_income_row is None:
        print("Warning: 'Median income (dollars)' row not found in second file")
    if mean_income_row is None:
        print("Warning: 'Mean income (dollars)' row not found in second file")
    
    # Create new columns for median and mean income in the first dataframe
    df1['Median_Income_Dollars'] = None
    df1['Mean_Income_Dollars'] = None
    
    # Process each row in the first CSV
    for idx, row in df1.iterrows():
        zcta5_value = str(row['ZCTA5']).zfill(5)  # Ensure 5 digits with leading zeros
        
        # Find matching ZCTA5 column in second file
        if zcta5_value in zcta5_codes:
            zcta5_col_idx = zcta5_codes.index(zcta5_value)
            zcta5_col = zcta5_columns[zcta5_col_idx]
            
            # Extract median income if row exists
            if median_income_row is not None:
                median_value = df2.loc[median_income_row, zcta5_col]
                # Clean the value (remove commas, convert to numeric)
                try:
                    if pd.notna(median_value) and str(median_value) != '':
                        median_clean = str(median_value).replace(',', '').replace('$', '')
                        df1.loc[idx, 'Median_Income_Dollars'] = float(median_clean)
                except (ValueError, TypeError):
                    print(f"Warning: Could not convert median income value '{median_value}' for ZCTA5 {zcta5_value}")
            
            # Extract mean income if row exists
            if mean_income_row is not None:
                mean_value = df2.loc[mean_income_row, zcta5_col]
                # Clean the value (remove commas, convert to numeric)
                try:
                    if pd.notna(mean_value) and str(mean_value) != '':
                        mean_clean = str(mean_value).replace(',', '').replace('$', '')
                        df1.loc[idx, 'Mean_Income_Dollars'] = float(mean_clean)
                except (ValueError, TypeError):
                    print(f"Warning: Could not convert mean income value '{mean_value}' for ZCTA5 {zcta5_value}")
    
    # Save the merged data
    print(f"Saving merged data to {output_path}...")
    df1.to_csv(output_path, index=False)
    
    # Print summary statistics
    matched_count = df1['Median_Income_Dollars'].notna().sum()
    total_count = len(df1)
    print(f"\nSummary:")
    print(f"Total rows in first file: {total_count}")
    print(f"Rows with matched income data: {matched_count}")
    print(f"Match rate: {matched_count/total_count*100:.1f}%")

# Example usage
if __name__ == "__main__":
    # Replace these paths with your actual file paths
    file1_path = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official'/'Ohio-Retail-Pharmacies-with-zcta-vote-ins.csv'
    file2_path = Path(__file__).parent.parent / 'Data' / 'ZCTA' /'ACSST5Y2023-household-income-zcta.csv' 
    output_path = Path(__file__).parent.parent / 'Data' / 'Pharmacy' / 'Official'/'Ohio-Retail-Pharmacies-with-zcta-vote-ins-hh.csv' 
    
    try:
        merge_income_data(file1_path, file2_path, output_path)
        print("Merge completed successfully!")
    except Exception as e:
        print(f"Error: {e}")