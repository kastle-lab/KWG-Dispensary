# Imports
import pandas as pd
import os
from pathlib import Path

# Functions
def filter_ohio_addresses(input_filename, output_filename=None):
    """
    Filter CSV to keep only addresses containing 'OH'
    
    Args:
        input_filename (str): Path to input CSV file
        output_filename (str): Path to output CSV file (optional)
    
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    
    # Check if input file exists
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' not found!")
        return None
    
    # Read the CSV file
    print(f"Reading data from '{input_filename}'...")
    try:
        df = pd.read_csv(input_filename)
        print(f"Original dataset: {len(df)} records")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None
    
    # Check if Address column exists
    if 'Address' not in df.columns:
        print("Error: 'Address' column not found in the CSV file!")
        print(f"Available columns: {list(df.columns)}")
        return None
    
    # Display sample of original addresses
    print(f"\nSample original addresses:")
    for i, addr in enumerate(df['Address'].head(5)):
        print(f"  {i+1}. {addr}")
    
    # Count records before filtering
    original_count = len(df)
    
    # Filter for addresses containing 'OH' (case-insensitive)
    # Using str.contains with case=False to handle variations like 'oh', 'Oh', 'OH'
    ohio_mask = df['Address'].str.contains('OH', case=False, na=False)
    df_filtered = df[ohio_mask].copy()
    
    # Count records after filtering
    filtered_count = len(df_filtered)
    removed_count = original_count - filtered_count
    
    # Display results
    print(f"\n=== FILTERING RESULTS ===")
    print(f"Original records: {original_count}")
    print(f"Records with 'OH' in address: {filtered_count}")
    print(f"Records removed: {removed_count}")
    print(f"Percentage kept: {(filtered_count/original_count)*100:.1f}%")
    
    # Show sample of filtered addresses
    if filtered_count > 0:
        print(f"\nSample filtered addresses:")
        for i, addr in enumerate(df_filtered['Address'].head(5)):
            print(f"  {i+1}. {addr}")
    
    # Show examples of removed addresses (if any)
    if removed_count > 0:
        non_ohio_mask = ~ohio_mask
        df_removed = df[non_ohio_mask]
        print(f"\nSample removed addresses (non-OH):")
        for i, addr in enumerate(df_removed['Address'].head(5)):
            print(f"  {i+1}. {addr}")
    
    # Save filtered data
    if output_filename is None:
        # Create output filename based on input filename
        base_name = os.path.splitext(input_filename)[0]
        output_filename = f"{base_name}-clean.csv"
    
    try:
        df_filtered.to_csv(output_filename, index=False)
        print(f"\nFiltered data saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving filtered data: {e}")
        return df_filtered
    
    # Display final statistics
    if filtered_count > 0:
        print(f"\n=== FINAL DATASET SUMMARY ===")
        print(f"Total Ohio pharmacies: {filtered_count}")
        
        # Show operational status breakdown if available
        if 'Operational_Status' in df_filtered.columns:
            status_counts = df_filtered['Operational_Status'].value_counts()
            print(f"\nOperational Status Breakdown:")
            for status, count in status_counts.items():
                print(f"  {status}: {count}")
        
        # Show top cities if possible to extract from addresses
        print(f"\nTop Ohio cities by pharmacy count:")
        try:
            # Extract city names (assuming format: "Address, City, OH ZIP")
            cities = df_filtered['Address'].str.extract(r', ([^,]+), OH')[0].value_counts().head(10)
            for city, count in cities.items():
                if pd.notna(city):
                    print(f"  {city}: {count} pharmacies")
        except:
            print("  Could not extract city information")
    
    return df_filtered

def main():
    """Main function to run the address filtering"""
    
    # Default input filename (from the previous script)
    input_file = Path(__file__).parent.parent / 'Data' / 'Pharmacy' /'ohio-pharmacies.csv' 
    
    # Check if the default file exists, otherwise ask user
    if not os.path.exists(input_file):
        print(f"Default file '{input_file}' not found.")
        
        # List CSV files in current directory
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        
        if csv_files:
            print("Available CSV files in current directory:")
            for i, file in enumerate(csv_files, 1):
                print(f"  {i}. {file}")
            
            # For automation, we'll use the first CSV file found
            input_file = csv_files[0]
            print(f"\nUsing: {input_file}")
        else:
            print("No CSV files found in current directory!")
            return
    
    # Run the filtering
    filtered_df = filter_ohio_addresses(input_file)
    
    if filtered_df is not None:
        print(f"\n✅ Filtering completed successfully!")
        print(f"Check the output file for your filtered Ohio pharmacy data.")
    else:
        print(f"\n❌ Filtering failed!")

# Run the script
if __name__ == "__main__":
    main()