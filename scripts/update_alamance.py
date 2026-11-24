import pandas as pd

# Load the eligibility review CSV
csv_path = "results/healthcare_eligibility_review.csv"

df = pd.read_csv(
    csv_path,
    dtype=str,
    keep_default_na=False
)

# Identify the exact Alamance Skin Center record
mask = (
    (df["victim"] == "Alamance Skin Center")
    & (df["incident-date"].str.startswith("2020-10-21"))
    & (
        df["uuid"]
        == "0a58bf26-77e9-57c4-afc0-6d0b8f44b657"
    )
)

# Safety check: exactly one record must match
assert mask.sum() == 1, "Expected exactly one Alamance record."

# Mark as eligible
df.loc[mask, "eligibility_status"] = "Eligible"
df.loc[mask, "exclusion_reason"] = ""

# Document the date discrepancy
df.loc[mask, "review_notes"] = (
    "Healthcare delivery organization associated with Cone Health. "
    "Ransomware affected the practice's systems and patient records. "
    "Reported attack occurred in late July 2020, while the dataset "
    "lists October 21, 2020. Date discrepancy documented; "
    "both dates fall within the 2020 study period."
)

# Record supporting source
df.loc[mask, "review_source"] = (
    "https://www.beckershospitalreview.com/cybersecurity/"
    "cone-health-unable-to-recover-patient-data-lost-in-ransomware-attack.html"
)

# Save the updated review file
df.to_csv(csv_path, index=False)

print("Alamance Skin Center marked as Eligible.")
print("Total records:", len(df))
print(
    "Eligible records:",
    (df["eligibility_status"] == "Eligible").sum()
)
print(
    "Excluded records:",
    (df["eligibility_status"] == "Excluded").sum()
)
print(
    "Alamance Skin Center status:",
    df.loc[mask, "eligibility_status"].iloc[0]
)
