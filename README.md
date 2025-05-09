﻿# Orion-Astrathon

NASA GeneLab Repository
NASA GeneLab is an open-access platform that hosts over 200 omics datasets from spaceflight and space-relevant experiments. It includes data from transcriptomics (RNA-seq and microarray), proteomics, metabolomics, and more. For instance, some of the popular datasets include:
GLDS-48: Rodent spaceflight data


GLDS-65: Microbial experiments


GLDS-123: Zebrafish omics data


GLDS-140 & GLDS-13: Human-derived experiments


These datasets are ideal for training and transfer learning in your Celestial BioML Model Hub project. You can browse and download data directly from the NASA GeneLab Data Repository.
 citeturn0search0
NASA Open Science Data Repository (OSDR)
Another option is the NASA OSDR, which aggregates diverse biological datasets from spaceflight experiments, including those processed via GeneLab. It’s a great resource if you’re looking to integrate various data types (e.g., omics with phenotypic and environmental data).
 citeturn0search8
Both sources provide standardized, curated data that can help reduce training costs and improve model performance via transfer learning approaches. Let me know if you need further details or help accessing specific datasets!
Below is an updated version of your script that checks for the existence of the "Parameter Value[Collection Dates]" column before trying to split it. This prevents the KeyError when the column isn’t present in your data. The script also uses a raw string for the Windows file path:
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

Explanation
File Path: The file path is now provided as a raw string (r"...") to handle Windows backslashes correctly.


Date Parsing: The script first checks if the column "Parameter Value[Collection Dates]" exists before attempting to parse it. If it isn’t present, it skips that step.


Column Renaming & Reordering: The renaming dictionary and desired column order are applied only to columns that actually exist in the DataFrame.


Output: The cleaned data is saved as a CSV file with a modified name.


Run this script in your Python environment, and it should process the data without raising a KeyError for the missing column.

