import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the file path (using a raw string for Windows path)
file_path = r"C:\Users\sambh\Downloads\orion\notebooks\s_OSD-168_cleaned.csv"

# Load the cleaned CSV file (no date parsing as no date columns are present)
df = pd.read_csv(file_path)

# Show basic summary statistics
print("Summary Statistics:")
print(df.describe(include='all'))
print("\nData Types:")
print(df.dtypes)

# ---------------------------
# Visualization: Sample Storage Temperature Distribution
# ---------------------------
plt.figure(figsize=(8, 4))
# Convert storage temperature to numeric if necessary
df["Sample Storage Temperature"] = pd.to_numeric(df["Sample Storage Temperature"], errors='coerce')
sns.histplot(df["Sample Storage Temperature"].dropna(), bins=5, kde=True, color="salmon")
plt.title("Distribution of Sample Storage Temperature")
plt.xlabel("Temperature (" + df["Unit"].iloc[0] + ")")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("storage_temperature_distribution.png")
plt.show()

# ---------------------------
# Visualization: Count of Samples by Organism and Preservation Method
# ---------------------------
plt.figure(figsize=(10, 6))
ax = sns.countplot(data=df, x="organism", hue="preservation_method", palette="Set2")
plt.title("Samples by Organism and Preservation Method")
plt.xlabel("Organism")
plt.ylabel("Count of Samples")
plt.xticks(rotation=45)
plt.legend(title="Preservation Method")
plt.tight_layout()
plt.savefig("samples_by_organism_preservation.png")
plt.show()

# ---------------------------
# Visualization: Count of Samples by Spaceflight Factor
# ---------------------------
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="spaceflight", palette="pastel")
plt.title("Count of Samples by Spaceflight Factor")
plt.xlabel("Spaceflight")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("samples_by_spaceflight.png")
plt.show()

# Save the updated DataFrame with extended metadata to CSV
output_file = r"C:\Users\sambh\Downloads\orion\notebooks\s_OSD-168_cleaned_extended.csv"
df.to_csv(output_file, index=False)
print("\nExtended cleaned metadata saved as 's_OSD-168_cleaned_extended.csv'.")
