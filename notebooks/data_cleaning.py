import pandas as pd
from datetime import datetime

# Define the file name (using a raw string to prevent escape issues)
file_name = r"C:\Users\sambh\Downloads\orion\data\OSD-168_metadata_OSD-168-ISA\s_OSD-168.txt"

# Read data into a DataFrame (assuming tab-separated values)
df = pd.read_csv(file_name, sep="\t")

print("Original Data:")
print(df.head(), "\n")

# Step 1: If 'Parameter Value[Collection Dates]' exists, split it into two separate columns
def parse_dates(date_str):
    try:
        start_str, end_str = date_str.split(" and ")
        start_date = datetime.strptime(start_str.strip(), "%d-%b-%Y")
        end_date = datetime.strptime(end_str.strip(), "%d-%b-%Y")
        return pd.Series({"Start Date": start_date, "End Date": end_date})
    except Exception:
        return pd.Series({"Start Date": pd.NaT, "End Date": pd.NaT})

if "Parameter Value[Collection Dates]" in df.columns:
    df[["Start Date", "End Date"]] = df["Parameter Value[Collection Dates]"].apply(parse_dates)
    # Drop the original column once parsed
    df.drop(columns=["Parameter Value[Collection Dates]"], inplace=True)
else:
    print("Column 'Parameter Value[Collection Dates]' not found; skipping date parsing.")

# Step 2: Convert 'Parameter Value[Sample Storage Temperature]' to numeric if it exists
if "Parameter Value[Sample Storage Temperature]" in df.columns:
    df["Sample Storage Temperature"] = pd.to_numeric(df["Parameter Value[Sample Storage Temperature]"], errors='coerce')
else:
    print("Column 'Parameter Value[Sample Storage Temperature]' not found; skipping temperature conversion.")

# Step 3: Rename columns for clarity (only rename columns that are present)
rename_dict = {
    "Source Name": "source_name",
    "Sample Name": "sample_name",
    "Characteristics[Organism]": "organism",
    "Characteristics[Material Type]": "material_type",  # if it exists
    "Factor Value[Spaceflight]": "spaceflight",            # if it exists
    "Protocol REF": "protocol",
    "Parameter Value[Sample Preservation Method]": "preservation_method"
}
# Filter out keys not in df.columns
rename_dict = {old: new for old, new in rename_dict.items() if old in df.columns}
df.rename(columns=rename_dict, inplace=True)

# Step 4: (Optional) Reorder columns for clarity, including only those that exist
desired_order = [
    "source_name", "sample_name", "organism", "material_type", "spaceflight",
    "protocol", "Start Date", "End Date", "preservation_method",
    "Sample Storage Temperature", "Unit"
]
cols_order = [col for col in desired_order if col in df.columns]
df = df[cols_order]

# Display the cleaned DataFrame
print("Cleaned Data:")
print(df)
    
# Save the cleaned DataFrame to CSV
output_file = file_name.replace(".txt", "_cleaned.csv")
df.to_csv(output_file, index=False)
print(f"\nCleaned data saved as '{output_file}'.")
