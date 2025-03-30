import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Specify the input file path (you can update this if needed)
input_file = r"C:\Users\sambh\Downloads\orion\notebooks\s_OSD-168_cleaned.csv"

# Create an 'analysis' directory in the current working directory
analysis_dir = os.path.join(os.getcwd(), "analysis")
if not os.path.exists(analysis_dir):
    os.makedirs(analysis_dir)

# Load the cleaned CSV file (no date parsing as no date columns are present)
df = pd.read_csv(input_file)

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
plt.savefig(os.path.join(analysis_dir, "storage_temperature_distribution.png"))
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
plt.savefig(os.path.join(analysis_dir, "samples_by_organism_preservation.png"))
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
plt.savefig(os.path.join(analysis_dir, "samples_by_spaceflight.png"))
plt.show()

# ---------------------------
# Additional Analysis
# ---------------------------

# 1. Average Sample Storage Temperature by Organism
grouped_temp = df.groupby("organism")["Sample Storage Temperature"].mean().reset_index()
print("Average Sample Storage Temperature by Organism:")
print(grouped_temp)

plt.figure(figsize=(8, 4))
sns.barplot(data=grouped_temp, x="organism", y="Sample Storage Temperature", palette="viridis")
plt.title("Average Sample Storage Temperature by Organism")
plt.xlabel("Organism")
plt.ylabel("Avg. Storage Temperature (" + df["Unit"].iloc[0] + ")")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(analysis_dir, "avg_storage_temperature_by_organism.png"))
plt.show()

# 2. Count of Samples by Protocol
plt.figure(figsize=(8, 4))
sns.countplot(data=df, x="protocol", palette="Set3")
plt.title("Count of Samples by Protocol")
plt.xlabel("Protocol")
plt.ylabel("Number of Samples")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(analysis_dir, "samples_by_protocol.png"))
plt.show()

# 3. Pivot Table: Sample Counts by Organism and Preservation Method
pivot_counts = pd.pivot_table(df, index="organism", columns="preservation_method", values="sample_name", aggfunc="count", fill_value=0)
print("Pivot Table: Sample Counts by Organism and Preservation Method:")
print(pivot_counts)

# 4. Heatmap of the Pivot Table
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_counts, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Heatmap: Sample Counts by Organism and Preservation Method")
plt.xlabel("Preservation Method")
plt.ylabel("Organism")
plt.tight_layout()
plt.savefig(os.path.join(analysis_dir, "heatmap_organism_preservation.png"))
plt.show()

# 5. Box Plot: Storage Temperature Distribution by Protocol
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="protocol", y="Sample Storage Temperature", palette="coolwarm")
plt.title("Storage Temperature Distribution by Protocol")
plt.xlabel("Protocol")
plt.ylabel("Sample Storage Temperature (" + df["Unit"].iloc[0] + ")")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(analysis_dir, "boxplot_temperature_by_protocol.png"))
plt.show()

# Save the extended DataFrame to CSV in the analysis directory
output_file = os.path.join(analysis_dir, "s_OSD-168_cleaned_extended.csv")
df.to_csv(output_file, index=False)
print("\nExtended cleaned metadata saved as 's_OSD-168_cleaned_extended.csv' in the analysis directory.")
