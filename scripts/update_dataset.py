
import pandas as pd
from pathlib import Path

# Location of the eligibility review CSV
file_path = Path("results/healthcare_eligibility_review.csv")

# Load the existing CSV
df = pd.read_csv(file_path, keep_default_na=False)

# Find the correct incident
mask = (
    (df["victim"] == "Dr Reddy's Laboratories")
    & (df["incident-date"].astype(str).str.startswith("2020-10-21"))
)

# Verify that exactly one record matches
if mask.sum() != 1:
    raise ValueError(
        f"Expected 1 matching incident, found {mask.sum()}"
    )

# Update the eligibility information
df.loc[mask, "eligibility_status"] = "Excluded"

df.loc[mask, "exclusion_reason"] = (
    "Pharmaceutical company; not a direct "
    "healthcare delivery organization"
)

df.loc[mask, "review_notes"] = (
    "Ransomware incident reported in October 2020. "
    "Excluded because the organization manufactures "
    "pharmaceutical products rather than directly "
    "providing patient care."
)

df.loc[mask, "review_source"] = (
    "https://www.drreddys.com/"
)

# Check the number of records before saving
if len(df) != 670:
    raise ValueError(
        f"Expected 670 records, found {len(df)}"
    )

# Save the updated eligibility review CSV
df.to_csv(file_path, index=False)

print("Dr Reddy's Laboratories marked as Excluded.")
print("Total records:", len(df))
print(
    "Excluded records:",
    (df["eligibility_status"] == "Excluded").sum()
)
