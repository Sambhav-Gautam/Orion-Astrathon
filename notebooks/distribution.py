import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned CSV file (created from previous code)
df = pd.read_csv("cleaned_space_biology_metadata.csv", parse_dates=["Start Date", "End Date"])

# Show basic summary statistics
print("Summary Statistics:")
print(df.describe(include='all'))
print("\nData Types:")
print(df.dtypes)

# ---------------------------
# Visualization 1: Distribution of Collection Dates
# ---------------------------
# For the timeline, we can use the "Start Date" column
plt.figure(figsize=(10, 4))
sns.histplot(df["Start Date"].dropna(), bins=10, kde=False, color="skyblue")
plt.title("Distribution of Collection Start Dates")
plt.xlabel("Start Date")
plt.ylabel("Number of Samples")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("collection_start_dates.png")
plt.show()

# ---------------------------
# Visualization 2: Sample Storage Temperature Distribution
# ---------------------------
plt.figure(figsize=(8, 4))
sns.histplot(df["Sample Storage Temperature"].dropna(), bins=5, kde=True, color="salmon")
plt.title("Distribution of Sample Storage Temperature")
plt.xlabel("Temperature (degree Celsius)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("storage_temperature_distribution.png")
plt.show()

# ---------------------------
# Visualization 3: Count of Samples by Organism and Preservation Method
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
# Visualization 4: Count of Samples by Spaceflight Factor
# ---------------------------
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="spaceflight", palette="pastel")
plt.title("Count of Samples by Spaceflight Factor")
plt.xlabel("Spaceflight")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("samples_by_spaceflight.png")
plt.show()

# ---------------------------
# Additional processing: Create a new column for duration (if End Date exists)
# ---------------------------
# Calculate the number of days between Start and End dates
df["Collection Duration (days)"] = (df["End Date"] - df["Start Date"]).dt.days
print("\nCollection Duration Summary:")
print(df["Collection Duration (days)"].describe())

# Plot the duration distribution if data is available
plt.figure(figsize=(8, 4))
sns.histplot(df["Collection Duration (days)"].dropna(), bins=5, kde=False, color="mediumpurple")
plt.title("Distribution of Collection Duration (days)")
plt.xlabel("Duration (days)")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("collection_duration_distribution.png")
plt.show()

# Save the updated DataFrame with new column back to CSV
df.to_csv("cleaned_space_biology_metadata_extended.csv", index=False)
print("\nExtended cleaned metadata saved as 'cleaned_space_biology_metadata_extended.csv'.")
