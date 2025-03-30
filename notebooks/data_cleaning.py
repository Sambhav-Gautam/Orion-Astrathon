import pandas as pd
from io import StringIO
from datetime import datetime

# Sample data provided as a multiline string (for demonstration)
data = """
Source Name\tSample Name\tCharacteristics[Organism]\tTerm Source REF\tTerm Accession Number\tCharacteristics[Material Type]\tTerm Source REF\tTerm Accession Number\tFactor Value[Spaceflight]\tTerm Source REF\tTerm Accession Number\tProtocol REF\tParameter Value[Collection Dates]\tParameter Value[Sample Preservation Method]\tTerm Source REF\tTerm Accession Number\tParameter Value[Sample Storage Temperature]\tUnit\tTerm Source REF\tTerm Accession Number
1-F4_S2\t1-F4_S2\tMicrobiota\tNCBITAXON\thttp://purl.bioontology.org/ontology/NCBITAXON/13613\tCells\tMESH\thttp://purl.bioontology.org/ontology/MESH/D002477\tSpace Flight\tMESH\thttp://purl.bioontology.org/ontology/MESH/D013026\tsample collection\t04-MAR-2015 and 15-MAY-2015\tsterile zip lock bag\tOSD\thttps://osdr.nasa.gov/\t4\tdegree Celsius\tUO\thttp://purl.obolibrary.org/obo/UO_0000027
1P-F4P_S1\t1P-F4P_S1\tMicrobiota\tNCBITAXON\thttp://purl.bioontology.org/ontology/NCBITAXON/13613\tCells\tMESH\thttp://purl.bioontology.org/ontology/MESH/D002477\tSpace Flight\tMESH\thttp://purl.bioontology.org/ontology/MESH/D013026\tsample collection\t04-MAR-2015 and 15-MAY-2015\tsterile zip lock bag\tOSD\thttps://osdr.nasa.gov/\t4\tdegree Celsius\tUO\thttp://purl.obolibrary.org/obo/UO_0000027
2-F5_S4\t2-F5_S4\tMicrobiota\tNCBITAXON\thttp://purl.bioontology.org/ontology/NCBITAXON/13613\tCells\tMESH\thttp://purl.bioontology.org/ontology/MESH/D002477\tSpace Flight\tMESH\thttp://purl.bioontology.org/ontology/MESH/D013026\tsample collection\t04-MAR-2015 and 15-MAY-2015\tsterile zip lock bag\tOSD\thttps://osdr.nasa.gov/\t4\tdegree Celsius\tUO\thttp://purl.obolibrary.org/obo/UO_0000027
2P-F5P_S3\t2P-F5P_S3\tMicrobiota\tNCBITAXON\thttp://purl.bioontology.org/ontology/NCBITAXON/13613\tCells\tMESH\thttp://purl.bioontology.org/ontology/MESH/D002477\tSpace Flight\tMESH\thttp://purl.bioontology.org/ontology/MESH/D013026\tsample collection\t04-MAR-2015 and 15-MAY-2015\tsterile zip lock bag\tOSD\thttps://osdr.nasa.gov/\t4\tdegree Celsius\tUO\thttp://purl.obolibrary.org/obo/UO_0000027
"""

# Read data into a DataFrame (assuming tab-separated values)
df = pd.read_csv(StringIO(data), sep="\t")

# Display the original DataFrame
print("Original Data:")
print(df.head(), "\n")

# Step 1: Split 'Parameter Value[Collection Dates]' into two separate columns
def parse_dates(date_str):
    # Expecting format "04-MAR-2015 and 15-MAY-2015"
    try:
        start_str, end_str = date_str.split(" and ")
        start_date = datetime.strptime(start_str.strip(), "%d-%b-%Y")
        end_date = datetime.strptime(end_str.strip(), "%d-%b-%Y")
        return pd.Series({"Start Date": start_date, "End Date": end_date})
    except Exception as e:
        # Return NaT if parsing fails
        return pd.Series({"Start Date": pd.NaT, "End Date": pd.NaT})

date_cols = df["Parameter Value[Collection Dates]"].apply(parse_dates)
df = pd.concat([df, date_cols], axis=1)

# Step 2: Convert the 'Parameter Value[Sample Storage Temperature]' to numeric (if not already)
df["Sample Storage Temperature"] = pd.to_numeric(df["Parameter Value[Sample Storage Temperature]"], errors='coerce')

# (Optional) Rename some columns to simplify further processing
df.rename(columns={
    "Source Name": "source_name",
    "Sample Name": "sample_name",
    "Characteristics[Organism]": "organism",
    "Characteristics[Material Type]": "material_type",
    "Factor Value[Spaceflight]": "spaceflight",
    "Protocol REF": "protocol",
    "Parameter Value[Sample Preservation Method]": "preservation_method"
}, inplace=True)

# Step 3: Drop the original 'Parameter Value[Collection Dates]' column if not needed anymore
df.drop(columns=["Parameter Value[Collection Dates]"], inplace=True)

# Step 4: (Optional) Reorder or select columns for clarity
cols_order = [
    "source_name", "sample_name", "organism", "material_type", "spaceflight",
    "protocol", "Start Date", "End Date", "preservation_method",
    "Sample Storage Temperature", "Unit"
]
df = df[cols_order]

# Display the cleaned DataFrame
print("Cleaned Data:")
print(df)

# Save the cleaned DataFrame to CSV for downstream processing
df.to_csv("cleaned_space_biology_metadata.csv", index=False)
print("\nCleaned data saved as 'cleaned_space_biology_metadata.csv'.")
